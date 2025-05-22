// services/PictureService.js
/* eslint-disable no-constant-condition, no-unused-vars */

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

// Get the API URL from environment variables or default to localhost with protocol
const API_URL = process.env.VUE_APP_SERVER_URL || 'http://localhost:5000';

// API endpoint for pictures - using relative path since we'll use AuthService for requests
const PICTURE_ENDPOINT = 'user/picture';

/**
 * Improved check if the browser supports AVIF using multiple detection methods
 * 
 * @returns {Promise<boolean>} True if AVIF is supported
 */
async function checkAvifSupport() {

  // Method 1: Feature detection via canvas
  try {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 1;

    // Try to check if canvas.toBlob supports AVIF
    if (canvas && canvas.getContext && canvas.toBlob) {
      return new Promise((resolve) => {
        try {
          canvas.toBlob((blob) => {
            if (blob) {
              resolve(true);  // If we can create any blob, we'll try AVIF later
            } else {
              resolve(false);
            }
          }, 'image/avif');
        } catch (e) {
          resolve(false);
        }
      });
    }
  } catch (e) {
    console.log('Canvas feature detection failed:', e);
  }

  // Method 2: Image decode test with a simple minimal AVIF image
  // This is a tiny valid AVIF image (1x1 pixel)
  const avifTestImages = [
    // Minimal AVIF image
    'data:image/avif;base64,AAAAGGZ0eXBhdmlmAAAAAG1pZjFtaWFmAAAA0m1ldGEAAAAAAAAAIWhkbHIAAAAAAAAAAHBpY3QAAAAAAAAAAAAAAAAAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAABcAAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAEAAAABAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQAMAAAAABNjb2xybmNseAACAAIABoAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAAB9tZGF0EgAKCBgABogQEDQgMgkQAAAAB8dSLZ0=',

    // Alternative test image (simpler)
    'data:image/avif;base64,AAAAHGZ0eXBhdmlmAAAAAG1pZjFtaWFmAAAAD21ldGEAAAAAAAAAIWhkbHIAAAAAAAAAAHBpY3QAAAAAAAAAAAAAAAAAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAABoAAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAEAAAABAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQ0MAAAAABNjb2xybmNseAACAAIABoAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAACBtZGF0EgAKCRgADIgw0IZcJxgQAAAAvGm9oA=='
  ];

  for (const testImage of avifTestImages) {
    try {
      const result = await new Promise((resolve) => {
        const img = new Image();

        // Set a reasonable timeout
        const timeout = setTimeout(() => {
          resolve(false);
        }, 1000);

        img.onload = () => {
          clearTimeout(timeout);
          resolve(img.width > 0 && img.height > 0);
        };

        img.onerror = () => {
          clearTimeout(timeout);
          resolve(false);
        };

        img.src = testImage;
      });

      if (result) {
        return true; // Successfully loaded an AVIF image
      }
    } catch (e) {
      console.log('Image decode test failed:', e);
    }
  }

  // Method 3: Simple feature detection
  // Check if image/avif is in the accepted types list
  try {
    if (self.createImageBitmap && 
        document.createElement('canvas').toDataURL('image/avif').indexOf('data:image/avif') === 0) {
      return true;
    }
  } catch (e) {
    console.log('HTMLImageElement.prototype.decode method failed:', e);
  }

  // All methods failed - AVIF is not supported
  console.log('All AVIF detection methods failed');
  return false;
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

  // If already AVIF, return the file as is
  if (file.type === 'image/avif') {
    const dimensions = await getImageDimensions(file);
    return { file, isAvif: true, dimensions };
  }

  // Check if browser supports AVIF
  const avifSupported = await checkAvifSupport();

  // If browser doesn't support AVIF, return the file as is
  if (!avifSupported) {
    const dimensions = await getImageDimensions(file);
    return { file, isAvif: false, dimensions };
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

    // Try AVIF first, then fall back to WebP if AVIF fails
    try {
      const avifBlob = await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error('Canvas.toBlob timed out'));
        }, 1000);

        canvas.toBlob((blob) => {
          clearTimeout(timeout);
          if (blob) {
            resolve(blob);
          } else {
            reject(new Error('Canvas.toBlob returned null'));
          }
        }, 'image/avif', config.quality / 100);
      });

      // Create File object from Blob
      const avifFile = new File([avifBlob], file.name.replace(/\.[^.]+$/, '.avif'), {
        type: 'image/avif',
        lastModified: Date.now()
      });

      // Get dimensions
      const dimensions = { width: canvas.width, height: canvas.height };
      return { file: avifFile, isAvif: true, dimensions };
    } catch (e) {
      console.log('AVIF conversion failed, falling back to original format:', e);
    }

    // If AVIF conversion fails, return original file
    const dimensions = { width: img.width, height: img.height };
    return { file, isAvif: false, dimensions };

  } catch (error) {
    console.error('Error in conversion process:', error);
    // Fall back to original file if conversion fails
    const dimensions = await getImageDimensions(file);
    return { file, isAvif: false, dimensions };
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
   * @param {string} pictureType Type of picture (avatar, cover, etc.)
   * @param {Object} options Additional options
   * @returns {Promise<Object>} Server response
   */
  async uploadPicture(file, pictureType = 'avatar', options = {}) {
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
   * @param {string} pictureType Type of picture (avatar, cover, etc.)
   * @param {string} filename Custom filename (optional)
   * @param {Object} options Additional options
   * @returns {Promise<Object>} Server response
   */
  async uploadPictureFromUrl(imageUrl, pictureType = 'avatar', filename = null, options = {}) {
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
   * Retrieve a picture from the server with streaming support
   * 
   * @param {number} userId User ID (defaults to authenticated user)
   * @param {string} pictureType Type of picture (avatar, cover, etc.)
   * @param {'blob'|'url'|'data-url'} returnType Format to return the image in
   * @param {Function} onProgress Progress callback (receives value from 0-100)
   * @returns {Promise<Blob|string>} Image as Blob, URL or data URL based on returnType
   */
  async retrievePicture(userId = null, pictureType = 'avatar', returnType = 'url', onProgress = null) {
    try {
      // Use AuthService for authenticated requests
      const response = await AuthService.request('get', PICTURE_ENDPOINT, null, {
        params: {
          picture_type: pictureType,
          user_id: userId || undefined
        },
        responseType: 'arraybuffer',
        onDownloadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const progress = Math.min(Math.round((progressEvent.loaded / progressEvent.total) * 100), 100);
            onProgress(progress);
          }
        }
      });

      // Create a blob with the array buffer response
      const blob = new Blob([response.data], { type: 'image/avif' });

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
  async deletePicture(pictureType = 'avatar') {
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

      // Log form data for debugging
      // for (let [key, value] of formData.entries()) {
      //   console.log(key, ':', value);
      // }

      // Upload with XHR for progress tracking
      const result = await new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();

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
        xhr.open('POST', `${API_URL}/${PICTURE_ENDPOINT}`);

        // Configure auth
        const token = AuthService.getAccessToken();
        if (token) {
          xhr.setRequestHeader('Authorization', `Bearer ${token}`);
        }
        xhr.send(formData);
      });

      // Update picture URL
      pictureUrl.value = await PictureService.retrievePicture(null, pictureType, 'url');

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
  async function uploadFromUrl(url, pictureType = 'avatar', filename = null, options = {}) {
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
    deletePicture: PictureService.deletePicture,
    isAvifSupported: PictureService.isAvifSupported,
    getConfig: PictureService.getConfig
  };
}

export default PictureService;
