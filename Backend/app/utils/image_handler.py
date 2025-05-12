import io
from typing import Optional, BinaryIO, AsyncGenerator
import asyncio
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse

from PIL import Image, UnidentifiedImageError
from sqlalchemy.ext.asyncio import AsyncSession
import asyncpg
from asyncpg import Connection

from ..core.picture_config import picture_config, get_allowed_mime_types, is_mime_type_allowed
from ..db.postgress.postgress_pool import init_pg_pool

# Get configuration values
CHUNK_SIZE = picture_config.chunk_size
MAX_IMAGE_SIZE = picture_config.max_size
ALLOWED_MIME_TYPES = get_allowed_mime_types()
AVIF_QUALITY = picture_config.avif_quality
MAX_WIDTH = picture_config.max_width
MAX_HEIGHT = picture_config.max_height
MIN_WIDTH = picture_config.min_width
MIN_HEIGHT = picture_config.min_height

async def validate_image(file: UploadFile, max_size: int = MAX_IMAGE_SIZE) -> None:
    """
    Validate an uploaded image file (type and size).

    Args:
        file: The uploaded file
        max_size: Maximum allowed file size in bytes

    Raises:
        HTTPException: If the file is not valid
    """
    # Check if file is an image
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    # Check if image type is supported
    if not is_mime_type_allowed(file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported image format. Supported formats: {', '.join(ALLOWED_MIME_TYPES)}"
        )

    # Check file size by reading chunks without loading the whole file
    size = 0
    # First, move to the beginning
    await file.seek(0)

    chunk = await file.read(CHUNK_SIZE)
    while chunk:
        size += len(chunk)
        if size > max_size:
            # Reset file pointer to beginning
            await file.seek(0)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image is too large. Maximum size is {max_size/1024/1024}MB"
            )
        chunk = await file.read(CHUNK_SIZE)

    # Reset file pointer to beginning
    await file.seek(0)

async def read_chunks(file: UploadFile) -> AsyncGenerator[bytes, None]:
    """
    Read a file in chunks.

    Args:
        file: The uploaded file

    Yields:
        Chunks of file data
    """
    await file.seek(0)

    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break
        yield chunk

async def stream_avif_to_db(
    db_session: AsyncSession,
    file: UploadFile,
    save_chunk_function: callable,
    user_id: int,
    picture_type: str = "profile",
    commit: bool = True
) -> Optional[object]:
    """
    Stream an already AVIF-formatted image file directly to the database in chunks.

    Args:
        db_session: SQLAlchemy async session
        file: The uploaded AVIF file
        save_chunk_function: Function to save chunks (must accept session, chunk, is_first, is_last, user_id, picture_type)
        user_id: User ID
        picture_type: Type of picture
        commit: Whether to commit the transaction

    Returns:
        The result object from the save operation
    """
    # Validate that it's actually an AVIF image
    if file.content_type != 'image/avif':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is not in AVIF format"
        )

    # Validate file
    await validate_image(file)

    try:
        result = None
        is_first_chunk = True

        # Try to get file size from content length header
        content_length = None
        try:
            if hasattr(file, 'size'):
                content_length = file.size
            elif hasattr(file, 'headers') and 'content-length' in file.headers:
                content_length = int(file.headers['content-length'])
        except (TypeError, ValueError):
            # If we can't get the size, we'll detect the end by empty chunk
            pass

        # Reset file pointer to beginning
        await file.seek(0)

        # Stream file directly to database in chunks
        total_bytes_read = 0
        async for chunk in read_chunks(file):
            # Update total bytes read
            total_bytes_read += len(chunk)

            # Check if this is the last chunk
            is_last_chunk = False
            if content_length is not None:
                is_last_chunk = total_bytes_read >= content_length
            else:
                # If we don't know the size, we'll need to look ahead
                # to see if there's more data
                next_chunk = await file.read(1)
                if not next_chunk:
                    is_last_chunk = True
                else:
                    # Put the byte back (if possible)
                    await file.seek(total_bytes_read)

            # Save this chunk
            result = await save_chunk_function(
                db_session,
                chunk,
                is_first_chunk,
                is_last_chunk,
                user_id,
                picture_type,
                commit=False  # Don't commit until the last chunk
            )

            is_first_chunk = False

            # If this was the last chunk, break
            if is_last_chunk:
                break

        # Final commit after all chunks are processed
        if commit and result:
            await db_session.commit()

        return result
    except Exception as e:
        if commit:
            await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving image: {str(e)}"
        )

async def convert_to_avif_and_save(
    db_session: AsyncSession,
    file: UploadFile,
    save_chunk_function: callable,
    user_id: int,
    picture_type: str = "profile",
    commit: bool = True,
    quality: int = AVIF_QUALITY
) -> Optional[object]:
    """
    Convert an image to AVIF format, then stream it to the database in chunks.

    Note: For conversion, we unfortunately need to load the whole image into memory first.
    This function minimizes memory usage for the saving part, but conversion itself requires
    the full image data.

    Args:
        db_session: SQLAlchemy async session
        file: The uploaded image file
        save_chunk_function: Function to save chunks
        user_id: User ID
        picture_type: Type of picture
        commit: Whether to commit the transaction
        quality: AVIF quality level (0-100)

    Returns:
        The result object from the save operation
    """
    # If already AVIF, use the direct streaming function
    if file.content_type == 'image/avif':
        return await stream_avif_to_db(
            db_session, file, save_chunk_function, user_id, picture_type, commit
        )

    # Validate file
    await validate_image(file)

    try:
        # Unfortunately, for conversion we need to read the whole file
        # This is a limitation of image processing libraries
        buffer = io.BytesIO()
        async for chunk in read_chunks(file):
            buffer.write(chunk)

        # Reset buffer to beginning
        buffer.seek(0)

        # Run conversion in a thread pool to not block the event loop
        loop = asyncio.get_event_loop()
        avif_data = await loop.run_in_executor(
            None, 
            lambda: _convert_image_to_avif(buffer, quality)
        )

        # Create a BytesIO buffer from the AVIF data to read in chunks
        avif_buffer = io.BytesIO(avif_data)
        result = None
        is_first_chunk = True

        # Stream the converted AVIF data in chunks
        while True:
            chunk = avif_buffer.read(CHUNK_SIZE)
            if not chunk:
                break

            # Check if this is the last chunk
            is_last_chunk = avif_buffer.tell() >= len(avif_data)

            # Save this chunk
            result = await save_chunk_function(
                db_session,
                chunk,
                is_first_chunk,
                is_last_chunk,
                user_id,
                picture_type,
                commit=False  # Don't commit until the last chunk
            )

            is_first_chunk = False

        # Final commit after all chunks are processed
        if commit:
            await db_session.commit()

        return result
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not identify image format"
        )
    except Exception as e:
        if commit:
            await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )
    finally:
        if 'buffer' in locals():
            buffer.close()
        if 'avif_buffer' in locals():
            avif_buffer.close()

def _convert_image_to_avif(image_data: BinaryIO, quality: int = AVIF_QUALITY) -> bytes:
    """
    Convert an image to AVIF format.

    Args:
        image_data: Binary data of the image
        quality: AVIF quality (0-100)

    Returns:
        The AVIF image data as bytes
    """
    try:
        with Image.open(image_data) as img:
            # Check dimensions
            width, height = img.size

            # Resize if necessary
            if width > MAX_WIDTH or height > MAX_HEIGHT:
                # Calculate new dimensions while preserving aspect ratio
                ratio = min(MAX_WIDTH / width, MAX_HEIGHT / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Check minimum dimensions
            if width < MIN_WIDTH or height < MIN_HEIGHT:
                raise ValueError(f"Image dimensions ({width}x{height}) are below minimum requirements ({MIN_WIDTH}x{MIN_HEIGHT})")

            # Create output buffer
            output = io.BytesIO()

            # Save as AVIF
            img.save(output, format="AVIF", quality=quality)

            # Get bytes
            output.seek(0)
            return output.getvalue()
    finally:
        # Ensure resources are properly cleaned up
        if 'output' in locals():
            output.close()

async def stream_image_from_db(
    conn: Connection,
    user_id: int,
    picture_type: str = "profile"
) -> AsyncGenerator[bytes, None]:
    """
    Stream an image directly from the database in chunks.

    Args:
        conn: AsyncPG connection
        user_id: User ID
        picture_type: Type of picture

    Yields:
        Chunks of image data
    """
    # Query to get the LO OID
    query = """
    SELECT picture_data FROM user_pictures 
    WHERE user_id = $1 AND type = $2
    """

    # First check if the record exists
    record = await conn.fetchrow(query, user_id, picture_type)

    if not record or not record['picture_data']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    # Stream the binary data in chunks
    image_data = record['picture_data']

    # Process in chunks
    for i in range(0, len(image_data), CHUNK_SIZE):
        yield image_data[i:i + CHUNK_SIZE]

async def get_streaming_response_for_image(
    user_id: int,
    picture_type: str = "profile"
) -> StreamingResponse:
    """
    Create a StreamingResponse for an image.

    Args:
        user_id: User ID
        picture_type: Type of picture

    Returns:
        StreamingResponse with the image
    """
    # Get a connection from the pool
    pool = await init_pg_pool()
    conn = None

    # We'll manage the connection explicitly to avoid leaks
    async def stream_generator():
        nonlocal conn
        try:
            # Acquire connection from pool
            conn = await pool.acquire()

            # Stream the image in chunks
            async for chunk in stream_image_from_db(conn, user_id, picture_type):
                yield chunk

        except Exception as e:
            # Log the error but don't raise - StreamingResponse can't handle exceptions after it starts
            print(f"Error in stream_generator: {e}")

        finally:
            # Always release the connection back to the pool
            if conn:
                await pool.release(conn)
                conn = None

    # Create the response
    response = StreamingResponse(
        stream_generator(),
        media_type="image/avif"
    )

    # Add a callback to ensure connection cleanup if the client disconnects
    # (This is a bit of a hack but necessary for proper cleanup)
    response.background = lambda: asyncio.create_task(ensure_connection_cleanup(conn, pool))

    return response

async def ensure_connection_cleanup(conn, pool):
    """Ensure the connection is released back to the pool"""
    if conn:
        try:
            await pool.release(conn)
        except Exception as e:
            print(f"Error releasing connection: {e}")
