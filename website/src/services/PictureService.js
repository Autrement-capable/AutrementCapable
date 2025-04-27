import { ref } from 'vue';
import AuthService from './AuthService';

// Default AVIF configuration
const DEFAULT_CONFIG = {
  maxSize: 5 * 1024 * 1024, // 5MB in bytes (from server config)
  maxWidth: 1920,           // Max width from server config
  maxHeight: 1080,          // Max height from server config
  minWidth: 100,            // Min width from server config
  minHeight: 100,           // Min height from server config
  quality: 70,              // AVIF quality (0-100) from server config
  chunkSize: 512 * 1024,    // Chunk size (not used client-side but for reference)
};

// API endpoint for pictures
const PICTURE_ENDPOINT = '/user/picture';

/**
 * Check if the browser supports AVIF
 * 
 * @returns {Promise<boolean>} True if AVIF is supported
 */
async function checkAvifSupport() {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve(img.width > 0 && img.height > 0);
    img.onerror = () => resolve(false);
    img.src = 'data:image/avif;base64,AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxbWlhZk1BMUEAAADybWV0YQAAAAAAAAAoaGRscgAAAAAAAAAAcGljdAAAAAAAAAAAAAAAAGxpYmF2aWYAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAAF0AAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAIAAAACAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQAMAAAAABNjb2xybmNseAACAAIABoAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAAGVtZGF0EgAKBzgADlgICAoXS';
  });
}

/**
 * Parse image dimensions from a File or Blob
 * 
 * @param {File|Blob} file Image file or blob
 * @returns {Promise<{width: number, height: number}>} Image dimensions
 */
async function getImageDimensions(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      resolve({
        width: img.width,
        height: img.height
      });
      URL.revokeObjectURL(img.src);
    };
    img.onerror = () => {
      URL.revokeObjectURL(img.src);
      reject(new Error('Failed to load image'));
    };
    img.src = URL.createObjectURL(file);
  });
}

/**
 * Resize an image to fit within max dimensions while maintaining aspect ratio
 * 
 * @param {HTMLImageElement} img Image element
 * @param {number} maxWidth Maximum width
 * @param {number} maxHeight Maximum height
 * @returns {HTMLCanvasElement} Canvas with resized image
 */
function resizeImage(img, maxWidth, maxHeight) {
  // Calculate new dimensions
  let { width, height } = img;

  if (width > maxWidth || height > maxHeight) {
    const ratio = Math.min(maxWidth / width, maxHeight / height);
    width = Math.floor(width * ratio);
    height = Math.floor(height * ratio);
  }

  // Create canvas and draw resized image
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;

  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, width, height);

  return canvas;
}

/**
 * Convert an image to AVIF format
 * 
 * @param {File|Blob} file Image file or blob
 * @param {Object} options Conversion options
 * @returns {Promise<{file: File, isAvif: boolean, dimensions: {width: number, height: number}}>} Result
 */
async function convertToAvif(file, options = {}) {
  // Merge options with defaults
  const config = { ...DEFAULT_CONFIG, ...options };

  // Check if browser supports AVIF
  const avifSupported = await checkAvifSupport();

  // If already AVIF or browser doesn't support AVIF, return the file as is
  if (file.type === 'image/avif' || !avifSupported) {
    // Still check dimensions for validation
    const dimensions = await getImageDimensions(file);

    // Validate dimensions
    if (dimensions.width < config.minWidth || dimensions.height < config.minHeight) {
      throw new Error(`Image dimensions (${dimensions.width}x${dimensions.height}) are too small. Minimum required is ${config.minWidth}x${config.minHeight}`);
    }

    return { 
      file, 
      isAvif: file.type === 'image/avif',
      dimensions
    };
  }

  try {
    // Load image for processing
    const img = await new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = URL.createObjectURL(file);
    });

    // Validate dimensions
    if (img.width < config.minWidth || img.height < config.minHeight) {
      URL.revokeObjectURL(img.src);
      throw new Error(`Image dimensions (${img.width}x${img.height}) are too small. Minimum required is ${config.minWidth}x${config.minHeight}`);
    }

    // Resize if needed
    const canvas = resizeImage(img, config.maxWidth, config.maxHeight);

    // Clean up image URL
    URL.revokeObjectURL(img.src);

    // Convert to AVIF
    const avifBlob = await new Promise((resolve, reject) => {
      canvas.toBlob(resolve, 'image/avif', config.quality / 100);
    });

    if (!avifBlob) { 
      throw new Error('Failed to convert image to AVIF format');
    }

    // Get dimensions of the resulting image
    const dimensions = {
      width: canvas.width,
      height: canvas.height
    };

    // Create File object from Blob
    const avifFile = new File([avifBlob], file.name.replace(/\.[^.]+$/, '.avif'), {
      type: 'image/avif',
      lastModified: Date.now()
    });

    return { 
      file: avifFile, 
      isAvif: true,
      dimensions
    };
  } catch (error) {
    console.error('Error converting to AVIF:', error);

    // Fall back to original file if conversion fails
    const dimensions = await getImageDimensions(file);
    return { 
      file, 
      isAvif: false,
      dimensions
    };
  }
}

/**
 * Fetch an image from a URL and return as a File object
 * 
 * @param {string} url Image URL
 * @param {string} filename Desired filename (optional)
 * @returns {Promise<File>} Image as File object
 */
async function fetchImageFromUrl(url, filename = null) {
  try {
    // Fetch the image
    const response = await fetch(url, { mode: 'cors' });

    if (!response.ok) {
      throw new Error(`Failed to fetch image: ${response.statusText}`);
    }

    // Get content type and generate filename if not provided
    const contentType = response.headers.get('content-type') || 'image/jpeg';
    const extension = contentType.split('/')[1] || 'jpg';
    const imageFilename = filename || `image_${Date.now()}.${extension}`;

    // Convert response to blob
    const blob = await response.blob();

    // Convert blob to File object
    return new File([blob], imageFilename, { 
      type: contentType,
      lastModified: Date.now()
    });
  } catch (error) {
    console.error('Error fetching image from URL:', error);
    throw error;
  }
}

const PictureService = {
  /**
   * Upload a picture to the server with automatic AVIF conversion if supported
   * 
   * @param {File|Blob} file Image file or blob
   * @param {string} pictureType Type of picture (profile, cover, etc.)
   * @param {Object} options Additional options
   * @returns {Promise<Object>} Server response
   */
  async uploadPicture(file, pictureType = 'profile', options = {}) {
    try {
      // First convert to AVIF if possible
      const { file: processedFile, isAvif, dimensions } = await convertToAvif(file, options);

      // Create form data
      const formData = new FormData();
      formData.append('picture', processedFile);
      formData.append('picture_type', pictureType);
      formData.append('is_avif', isAvif);

      // Add quality if specified
      if (options.quality) {
        formData.append('quality', options.quality);
      }

      // Send to server using authenticated request
      const response = await AuthService.request('post', PICTURE_ENDPOINT, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      return {
        ...response.data,
        dimensions
      };
    } catch (error) {
      console.error('Error uploading picture:', error);
      throw error;
    }
  },

  /**
   * Upload an image from a URL to the server
   * 
   * @param {string} imageUrl URL of the image
   * @param {string} pictureType Type of picture (profile, cover, etc.)
   * @param {string} filename Custom filename (optional)
   * @param {Object} options Additional options
   * @returns {Promise<Object>} Server response
   */
  async uploadPictureFromUrl(imageUrl, pictureType = 'profile', filename = null, options = {}) {
    try {
      // First fetch the image
      const imageFile = await fetchImageFromUrl(imageUrl, filename);

      // Then upload using our standard method
      return await this.uploadPicture(imageFile, pictureType, options);
    } catch (error) {
      console.error('Error uploading picture from URL:', error);
      throw error;
    }
  },

  /**
   * Get the URL for a user's picture
   * 
   * @param {number} userId User ID (defaults to authenticated user)
   * @param {string} pictureType Type of picture (profile, cover, etc.)
   * @returns {string} Picture URL with cache-busting parameter
   */
  getPictureUrl(userId = null, pictureType = 'profile') {
    // Add cache-busting parameter to prevent caching
    const cacheBuster = `_cb=${Date.now()}`;

    if (userId) {
      // For other users' pictures (if API supports this)
      // not implemented for now
    } else {
      // For current user's picture
      return `${PICTURE_ENDPOINT}?picture_type=${pictureType}&${cacheBuster}`;
    }
  },

  /**
   * Retrieve a picture from the server with streaming support
   * 
   * @param {number} userId User ID (defaults to authenticated user)
   * @param {string} pictureType Type of picture (profile, cover, etc.)
   * @param {'blob'|'url'|'data-url'} returnType Format to return the image in
   * @param {Function} onProgress Progress callback (receives value from 0-100)
   * @returns {Promise<Blob|string>} Image as Blob, URL or data URL based on returnType
   */
  async retrievePicture(userId = null, pictureType = 'profile', returnType = 'blob', onProgress = null) {
    try {
      // Create request options with authorization
      const options = {
        method: 'GET',
        headers: {}
      };

      // Add authorization if we have a token
      const token = AuthService.getAccessToken();
      if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
      }

      // Build URL
      let url = `${PICTURE_ENDPOINT}?picture_type=${pictureType}`;
      if (userId) {
        url += `&user_id=${userId}`;
      }

      // Make fetch request - this will receive a streaming response
      const response = await fetch(url, options);

      // Check if image exists
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Image not found');
        }
        throw new Error(`Failed to fetch image: ${response.statusText}`);
      }

      // Get total size from Content-Length header if available
      const contentLength = response.headers.get('Content-Length');
      const totalSize = contentLength ? parseInt(contentLength, 10) : 0;

      // Initialize for streaming
      let receivedSize = 0;
      const chunks = [];

      // Process the stream
      const reader = response.body.getReader();

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        // Add this chunk
        chunks.push(value);

        // Update received size and report progress
        receivedSize += value.length;

        if (onProgress && totalSize) {
          const progress = Math.min(Math.round((receivedSize / totalSize) * 100), 100);
          onProgress(progress);
        }
      }

      // Combine all chunks into a single Uint8Array
      const chunksAll = new Uint8Array(receivedSize);
      let position = 0;
      for (const chunk of chunks) {
        chunksAll.set(chunk, position);
        position += chunk.length;
      }

      // Create a blob with the correct MIME type
      const blob = new Blob([chunksAll], { type: 'image/avif' });

      // Return based on requested format
      if (returnType === 'blob') {
        return blob;
      } else if (returnType === 'url') {
        return URL.createObjectURL(blob);
      } else if (returnType === 'data-url') {
        return await new Promise((resolve) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result);
          reader.readAsDataURL(blob);
        });
      }

      // Default fallback
      return blob;
    } catch (error) {
      console.error('Error retrieving picture:', error);
      throw error;
    }
  },

  /**
   * Delete a user's picture
   * 
   * @param {string} pictureType Type of picture to delete
   * @returns {Promise<Object>} Server response
   */
  async deletePicture(pictureType = 'profile') {
    try {
      const response = await AuthService.request('delete', PICTURE_ENDPOINT, null, {
        params: { picture_type: pictureType }
      });

      return response.data;
    } catch (error) {
      console.error('Error deleting picture:', error);
      throw error;
    }
  },

  /**
   * Check if browser supports AVIF format
   * 
   * @returns {Promise<boolean>} True if AVIF is supported
   */
  async isAvifSupported() {
    return await checkAvifSupport();
  },

  /**
   * Get configuration for image handling
   * Including max/min dimensions, quality settings, etc.
   * 
   * @returns {Object} Current configuration
   */
  getConfig() {
    return { ...DEFAULT_CONFIG };
  }
};

/**
 * Vue composable for picture handling with reactive state
 * 
 * @returns {Object} Picture handling utilities with reactive state
 */
export function usePicture() {
  const isUploading = ref(false);
  const progress = ref(0);
  const error = ref(null);
  const pictureUrl = ref(null);

  /**
   * Upload a picture with progress tracking
   * 
   * @param {File|Blob} file Image file or blob
   * @param {string} pictureType Type of picture
   * @param {Object} options Additional options
   * @returns {Promise<Object>} Upload result
   */
  async function uploadPicture(file, pictureType = 'profile', options = {}) {
    isUploading.value = true;
    progress.value = 0;
    error.value = null;

    try {
      // Conversion progress (30%)
      progress.value = 10;
      const { file: processedFile, isAvif, dimensions } = await convertToAvif(file, options);
      progress.value = 30;

      // Create form data
      const formData = new FormData();
      formData.append('picture', processedFile);
      formData.append('picture_type', pictureType);
      formData.append('is_avif', isAvif);

      // Add quality if specified
      if (options.quality) {
        formData.append('quality', options.quality);
      }

      // Upload with XHR for progress tracking
      const result = await new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();

        // Configure auth
        const token = AuthService.getAccessToken();
        if (token) {
          xhr.setRequestHeader('Authorization', `Bearer ${token}`);
        }

        // Track upload progress
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable) {
            // Scale progress from 30% to 90%
            const uploadProgress = 30 + (event.loaded / event.total) * 60;
            progress.value = Math.min(90, uploadProgress);
          }
        });

        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            progress.value = 100;
            resolve({
              data: JSON.parse(xhr.responseText),
              dimensions
            });
          } else {
            try {
              reject(JSON.parse(xhr.responseText));
            } catch (e) {
              reject({ detail: 'Upload failed' });
            }
          }
        };

        xhr.onerror = () => reject({ detail: 'Network error during upload' });

        // Prepare and send the request
        xhr.open('POST', PictureService.getPictureUrl(null, pictureType));
        xhr.send(formData);
      });

      // Update picture URL
      pictureUrl.value = PictureService.getPictureUrl(null, pictureType);

      return result;
    } catch (err) {
      error.value = err.detail || err.message || 'Upload failed';
      throw err;
    } finally {
      isUploading.value = false;
    }
  }

  /**
   * Upload a picture from URL with progress tracking
   * 
   * @param {string} url Image URL
   * @param {string} pictureType Type of picture
   * @param {string} filename Custom filename (optional)
   * @param {Object} options Additional options
   * @returns {Promise<Object>} Upload result
   */
  async function uploadFromUrl(url, pictureType = 'profile', filename = null, options = {}) {
    isUploading.value = true;
    progress.value = 0;
    error.value = null;

    try {
      // Fetching image (20%)
      progress.value = 5;
      const imageFile = await fetchImageFromUrl(url, filename);
      progress.value = 20;

      // Upload using our standard method (remaining 80%)
      const result = await uploadPicture(imageFile, pictureType, options);

      return result;
    } catch (err) {
      error.value = err.detail || err.message || 'URL fetch failed';
      throw err;
    } finally {
      isUploading.value = false;
    }
  }

  return {
    // Reactive state
    isUploading,
    progress,
    error,
    pictureUrl,

    // Methods
    uploadPicture,
    uploadFromUrl,
    retrievePicture: PictureService.retrievePicture,
    getPictureUrl: PictureService.getPictureUrl,
    deletePicture: PictureService.deletePicture,
    isAvifSupported: PictureService.isAvifSupported,
    getConfig: PictureService.getConfig
  };
}

export default PictureService;
