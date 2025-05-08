// components/PictureServiceTester.vue
<template>
    <div class="picture-service-tester">
      <h2>Picture Service Tester</h2>
      
      <!-- Tabs for different test sections -->
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id" 
          :class="['tab-button', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>
      
      <!-- Tab content -->
      <div class="tab-content">
        <!-- Upload from File tab -->
        <div v-if="activeTab === 'upload-file'" class="upload-section">
          <h3>Upload Image File</h3>
          <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleFileDrop">
            <div v-if="!fileUploadProgress" class="upload-prompt">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24">
                <path d="M9 16h6v-6h4l-7-7-7 7h4v6zm-4 2h14v2H5v-2z"/>
              </svg>
              <p>Drag and drop an image here or click to select</p>
              <input 
                ref="fileInput"
                type="file" 
                accept="image/*" 
                style="display: none" 
                @change="handleFileSelect"
              />
            </div>
            <div v-else-if="fileUploadProgress < 100" class="upload-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${fileUploadProgress}%` }"></div>
              </div>
              <p>Uploading... {{ fileUploadProgress }}%</p>
            </div>
            <div v-else-if="uploadedImageUrl" class="upload-success">
              <img :src="uploadedImageUrl" alt="Uploaded image" class="preview-image" />
              <p>Upload successful!</p>
              <div class="image-info">
                <p><strong>Dimensions:</strong> {{ uploadedImageDimensions.width }} x {{ uploadedImageDimensions.height }}</p>
                <p><strong>Format:</strong> AVIF</p>
              </div>
            </div>
          </div>
          
          <div class="upload-options">
            <div class="form-group">
              <label for="picture-type">Picture Type:</label>
              <select id="picture-type" v-model="pictureType">
                <option value="profile">Profile</option>
                <option value="cover">Cover</option>
                <option value="avatar">Avatar</option>
              </select>
            </div>
            <div class="form-group">
              <label for="quality">AVIF Quality (0-100):</label>
              <input type="range" id="quality" v-model.number="quality" min="0" max="100" step="5" />
              <span>{{ quality }}</span>
            </div>
          </div>
          
          <div v-if="fileUploadError" class="error-message">
            {{ fileUploadError }}
          </div>
        </div>
        
        <!-- Upload from URL tab -->
        <div v-if="activeTab === 'upload-url'" class="upload-url-section">
          <h3>Upload Image from URL</h3>
          <div class="form-group">
            <label for="image-url">Image URL:</label>
            <input 
              type="url" 
              id="image-url" 
              v-model="imageUrl" 
              placeholder="https://example.com/image.jpg"
              :disabled="urlUploadProgress > 0 && urlUploadProgress < 100"
            />
          </div>
          
          <div class="form-group">
            <label for="url-picture-type">Picture Type:</label>
            <select id="url-picture-type" v-model="pictureType" :disabled="urlUploadProgress > 0 && urlUploadProgress < 100">
              <option value="profile">Profile</option>
              <option value="cover">Cover</option>
              <option value="avatar">Avatar</option>
            </select>
          </div>
          
          <button 
            @click="uploadFromUrl" 
            class="upload-button"
            :disabled="!imageUrl || (urlUploadProgress > 0 && urlUploadProgress < 100)"
          >
            {{ urlUploadProgress > 0 && urlUploadProgress < 100 ? `Uploading... ${urlUploadProgress}%` : 'Upload from URL' }}
          </button>
          
          <div v-if="urlUploadProgress === 100 && uploadedImageUrl" class="upload-success">
            <img :src="uploadedImageUrl" alt="Uploaded image" class="preview-image" />
            <p>Upload successful!</p>
            <div class="image-info">
              <p><strong>Dimensions:</strong> {{ uploadedImageDimensions.width }} x {{ uploadedImageDimensions.height }}</p>
              <p><strong>Format:</strong> AVIF</p>
            </div>
          </div>
          
          <div v-if="urlUploadError" class="error-message">
            {{ urlUploadError }}
          </div>
        </div>
        
        <!-- Retrieve Images tab -->
        <div v-if="activeTab === 'retrieve'" class="retrieve-section">
          <h3>Retrieve Images</h3>
          
          <div class="retrieve-options">
            <div class="form-group">
              <label for="retrieve-picture-type">Picture Type:</label>
              <select id="retrieve-picture-type" v-model="retrievePictureType" :disabled="isRetrieving">
                <option value="profile">Profile</option>
                <option value="cover">Cover</option>
                <option value="avatar">Avatar</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="retrieve-format">Return Format:</label>
              <select id="retrieve-format" v-model="retrieveFormat" :disabled="isRetrieving">
                <option value="url">Object URL</option>
                <option value="data-url">Data URL</option>
                <option value="blob">Blob</option>
              </select>
            </div>
          </div>
          
          <button 
            @click="retrieveImage" 
            class="retrieve-button"
            :disabled="isRetrieving"
          >
            {{ isRetrieving ? `Retrieving... ${retrieveProgress}%` : 'Retrieve Image' }}
          </button>
          
          <div v-if="retrieveError" class="error-message">
            {{ retrieveError }}
          </div>
          
          <div v-if="retrievedImageData && !retrieveError" class="retrieve-result">
            <h4>Retrieved Image:</h4>
            
            <div v-if="retrieveFormat === 'blob'" class="blob-info">
              <p><strong>Blob Size:</strong> {{ formatFileSize(retrievedImageData.size) }}</p>
              <p><strong>MIME Type:</strong> {{ retrievedImageData.type }}</p>
              <button @click="showBlobImage" class="view-blob-button">View Image</button>
            </div>
            
            <div v-else-if="retrieveFormat === 'data-url'" class="data-url-info">
              <p><strong>Data URL Length:</strong> {{ formatDataUrlLength(retrievedImageData) }}</p>
              <div class="truncated-data-url">{{ truncateDataUrl(retrievedImageData) }}</div>
              <img :src="retrievedImageData" alt="Retrieved image" class="preview-image" />
            </div>
            
            <div v-else class="url-preview">
              <img :src="retrievedImageData" alt="Retrieved image" class="preview-image" />
            </div>
          </div>
        </div>
        
        <!-- Delete tab -->
        <div v-if="activeTab === 'delete'" class="delete-section">
          <h3>Delete Images</h3>
          
          <div class="current-images">
            <div class="image-type-card" v-for="type in pictureTypes" :key="type">
              <h4>{{ type.charAt(0).toUpperCase() + type.slice(1) }}</h4>
              <div class="image-container">
                <img 
                  v-if="loadedImages[type]"
                  :src="imageUrls[type]" 
                  :alt="`${type} image`"
                  @error="imageLoadError($event, type)"
                  class="type-image"
                />
                <div class="image-overlay" v-if="loadedImages[type]">
                  <button @click="deleteImage(type)" class="delete-button">Delete</button>
                </div>
                <div v-if="loadingImages[type]" class="image-loading">
                  <div class="loading-spinner"></div>
                  <p>Loading...</p>
                </div>
                <div v-if="!loadedImages[type] && !loadingImages[type]" class="no-image">
                  No image found
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="deleteError" class="error-message">
            {{ deleteError }}
          </div>
          
          <div v-if="deleteSuccess" class="success-message">
            {{ deleteSuccess }}
          </div>
        </div>
        
        <!-- Browser Capabilities tab -->
        <div v-if="activeTab === 'capabilities'" class="capabilities-section">
          <h3>Browser Capabilities</h3>
          
          <div class="capability-card">
            <h4>AVIF Support</h4>
            <div class="capability-status">
              <div v-if="avifSupport === null" class="checking">Checking...</div>
              <div v-else-if="avifSupport" class="supported">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
                Supported
              </div>
              <div v-else class="not-supported">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
                Not Supported
              </div>
            </div>
            <p class="capability-description">
              AVIF is a modern image format that offers better compression and quality compared to JPEG and PNG.
              <span v-if="!avifSupport && avifSupport !== null">
                Your browser doesn't support AVIF natively. The service will use the original format or convert server-side.
              </span>
            </p>
          </div>
          
          <div class="server-config">
            <h4>Server Configuration</h4>
            <table>
              <tbody>
                <tr>
                  <td>Max Width:</td>
                  <td>{{ config.maxWidth }}px</td>
                </tr>
                <tr>
                  <td>Max Height:</td>
                  <td>{{ config.maxHeight }}px</td>
                </tr>
                <tr>
                  <td>Min Width:</td>
                  <td>{{ config.minWidth }}px</td>
                </tr>
                <tr>
                  <td>Min Height:</td>
                  <td>{{ config.minHeight }}px</td>
                </tr>
                <tr>
                  <td>Max File Size:</td>
                  <td>{{ formatFileSize(config.maxSize) }}</td>
                </tr>
                <tr>
                  <td>Default AVIF Quality:</td>
                  <td>{{ config.quality }}%</td>
                </tr>
                <tr>
                  <td>Server Chunk Size:</td>
                  <td>{{ formatFileSize(config.chunkSize) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue';
  import PictureService, { usePicture } from '../services/PictureService';

  // Get the API URL from environment or use default
  const API_URL = process.env.VUE_APP_SERVER_URL || 'http://localhost:5000';
  
  export default {
    name: 'PictureServiceTester',
    setup() {
      // Tabs
      const tabs = [
        { id: 'upload-file', label: 'Upload File' },
        { id: 'upload-url', label: 'Upload from URL' },
        { id: 'retrieve', label: 'Retrieve Images' },
        { id: 'delete', label: 'Delete Images' },
        { id: 'capabilities', label: 'Capabilities' }
      ];
      const activeTab = ref('upload-file');
      
      // File upload
      const fileInput = ref(null);
      const pictureType = ref('profile');
      const quality = ref(70);
      const fileUploadProgress = ref(0);
      const fileUploadError = ref('');
      const uploadedImageUrl = ref('');
      const uploadedImageDimensions = ref({ width: 0, height: 0 });
      
      // URL upload
      const imageUrl = ref('');
      const urlUploadProgress = ref(0);
      const urlUploadError = ref('');
      
      // Retrieve image
      const retrievePictureType = ref('profile');
      const retrieveFormat = ref('url');
      const isRetrieving = ref(false);
      const retrieveProgress = ref(0);
      const retrieveError = ref('');
      const retrievedImageData = ref(null);
      
      // Delete image
      const pictureTypes = ['profile', 'cover', 'avatar'];
      const loadedImages = reactive({});
      const loadingImages = reactive({});
      const imageUrls = reactive({});
      const deleteError = ref('');
      const deleteSuccess = ref('');
      
      // Browser capabilities
      const avifSupport = ref(null);
      const config = ref({});
      
      // Use composable
      const { 
        uploadPicture, uploadFromUrl: uploadPictureFromUrl, retrievePicture
      } = usePicture();
      
      // Load an image using PictureService
      const loadImage = async (type) => {
        loadingImages[type] = true;
        loadedImages[type] = false;
        
        try {
          const imageUrl = await PictureService.retrievePicture(null, type, 'url');
          imageUrls[type] = imageUrl;
          loadedImages[type] = true;
        } catch (error) {
          console.error(`Error loading ${type} image:`, error);
          loadedImages[type] = false;
        } finally {
          loadingImages[type] = false;
        }
      };
      
      // Methods for file upload
      const triggerFileInput = () => {
        if (fileInput.value) {
          fileInput.value.click();
        }
      };
      
      const handleFileSelect = async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        
        fileUploadError.value = '';
        fileUploadProgress.value = 1;
        
        try {
          const options = { quality: quality.value };
          
          // Upload image
          const result = await uploadPicture(
            file, 
            pictureType.value, 
            options
          );
          
          // Update UI with result - use PictureService to retrieve the uploaded image
          uploadedImageUrl.value = await PictureService.retrievePicture(null, pictureType.value, 'url');
          uploadedImageDimensions.value = result.dimensions;
          fileUploadProgress.value = 100;
          
          // Reload the image in the delete tab if it's the same type
          if (loadedImages[pictureType.value] !== undefined) {
            await loadImage(pictureType.value);
          }
        } catch (error) {
          fileUploadError.value = error.message || 'Upload failed';
          fileUploadProgress.value = 0;
        }
      };
      
      const handleFileDrop = (event) => {
        event.preventDefault();
        
        const file = event.dataTransfer.files[0];
        if (!file || !file.type.startsWith('image/')) return;
        
        // Create a new file input event
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        
        if (fileInput.value) {
          fileInput.value.files = dataTransfer.files;
          handleFileSelect({ target: { files: dataTransfer.files } });
        }
      };
      
      // Method for URL upload
      const uploadFromUrl = async () => {
        if (!imageUrl.value) return;
        
        urlUploadError.value = '';
        urlUploadProgress.value = 1;
        
        try {
          // Upload image from URL
          const result = await uploadPictureFromUrl(
            imageUrl.value,
            pictureType.value,
            null,
            { quality: quality.value }
          );
          
          // Update UI with result - use PictureService to retrieve the uploaded image
          uploadedImageUrl.value = await PictureService.retrievePicture(null, pictureType.value, 'url');
          uploadedImageDimensions.value = result.dimensions;
          urlUploadProgress.value = 100;
          
          // Reload the image in the delete tab if it's the same type
          if (loadedImages[pictureType.value] !== undefined) {
            await loadImage(pictureType.value);
          }
        } catch (error) {
          urlUploadError.value = error.message || 'Upload failed';
          urlUploadProgress.value = 0;
        }
      };
      
      // Method for retrieving images
      const retrieveImage = async () => {
        retrieveError.value = '';
        isRetrieving.value = true;
        retrieveProgress.value = 0;
        retrievedImageData.value = null;
        
        try {
          // Retrieve image with progress tracking
          const result = await retrievePicture(
            null, // Current user
            retrievePictureType.value,
            retrieveFormat.value,
            (progress) => {
              retrieveProgress.value = progress;
            }
          );
          
          // Store the result
          retrievedImageData.value = result;
        } catch (error) {
          retrieveError.value = error.message || 'Failed to retrieve image';
        } finally {
          isRetrieving.value = false;
        }
      };
      
      // Show blob image in new tab
      const showBlobImage = () => {
        if (!retrievedImageData.value || !(retrievedImageData.value instanceof Blob)) return;
        
        const url = URL.createObjectURL(retrievedImageData.value);
        window.open(url, '_blank');
        
        // Clean up the URL object after 5 seconds
        setTimeout(() => URL.revokeObjectURL(url), 5000);
      };
      
      // Method for deleting images
      const deleteImage = async (type) => {
        deleteError.value = '';
        deleteSuccess.value = '';
        
        try {
          await PictureService.deletePicture(type);
          loadedImages[type] = false;
          // Clean up the object URL if it exists
          if (imageUrls[type] && imageUrls[type].startsWith('blob:')) {
            URL.revokeObjectURL(imageUrls[type]);
          }
          imageUrls[type] = null;
          deleteSuccess.value = `${type.charAt(0).toUpperCase() + type.slice(1)} image deleted successfully`;
        } catch (error) {
          deleteError.value = error.message || 'Failed to delete image';
        }
      };
      
      // Handle image load error
      const imageLoadError = (event, type) => {
        loadedImages[type] = false;
        loadingImages[type] = false;
      };
      
      // Format file size
      const formatFileSize = (bytes) => {
        if (bytes < 1024) return bytes + ' B';
        else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
        else return (bytes / 1048576).toFixed(1) + ' MB';
      };
      
      // Format data URL length
      const formatDataUrlLength = (dataUrl) => {
        if (!dataUrl) return '0 B';
        return formatFileSize(dataUrl.length);
      };
      
      // Truncate data URL for display
      const truncateDataUrl = (dataUrl) => {
        if (!dataUrl) return '';
        return dataUrl.substring(0, 50) + '...' + dataUrl.substring(dataUrl.length - 20);
      };
      
      // Initialize
      onMounted(async () => {
        // Check AVIF support
        avifSupport.value = await PictureService.isAvifSupported();
        
        // Get service configuration
        config.value = PictureService.getConfig();
        
        // Load which images exist using the PictureService
        for (const type of pictureTypes) {
          loadingImages[type] = true;
          try {
            const imageUrl = await PictureService.retrievePicture(null, type, 'url');
            imageUrls[type] = imageUrl;
            loadedImages[type] = true;
          } catch (error) {
            loadedImages[type] = false;
          } finally {
            loadingImages[type] = false;
          }
        }
      });
      
      return {
        // State
        tabs,
        activeTab,
        fileInput,
        pictureType,
        quality,
        fileUploadProgress,
        fileUploadError,
        uploadedImageUrl,
        uploadedImageDimensions,
        imageUrl,
        urlUploadProgress,
        urlUploadError,
        retrievePictureType,
        retrieveFormat,
        isRetrieving,
        retrieveProgress,
        retrieveError,
        retrievedImageData,
        pictureTypes,
        loadedImages,
        loadingImages,
        imageUrls,
        deleteError,
        deleteSuccess,
        avifSupport,
        config,
        API_URL,
        
        // Methods
        triggerFileInput,
        handleFileSelect,
        handleFileDrop,
        uploadFromUrl,
        retrieveImage,
        showBlobImage,
        deleteImage,
        imageLoadError,
        formatFileSize,
        formatDataUrlLength,
        truncateDataUrl
      };
    }
  };
  </script>
  
  <style scoped>
  .picture-service-tester {
    padding: 20px;
  }
  
  h2 {
    margin-top: 0;
    margin-bottom: 25px;
    text-align: center;
  }
  
  /* Tabs */
  .tabs {
    display: flex;
    border-bottom: 1px solid #ddd;
    margin-bottom: 20px;
  }
  
  .tab-button {
    padding: 10px 20px;
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s;
  }
  
  .tab-button:hover {
    background-color: #f5f5f5;
  }
  
  .tab-button.active {
    border-bottom-color: #2196f3;
    color: #2196f3;
    font-weight: bold;
  }
  
  /* Tab content */
  .tab-content {
    background-color: white;
    border-radius: 4px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  h3 {
    margin-top: 0;
    margin-bottom: 20px;
    color: #333;
  }
  
  /* Upload file section */
  .upload-area {
    border: 2px dashed #ccc;
    border-radius: 8px;
    padding: 30px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.3s;
    margin-bottom: 20px;
    background-color: #fafafa;
  }
  
  .upload-area:hover {
    border-color: #2196f3;
  }
  
  .upload-prompt svg {
    fill: #999;
    margin-bottom: 10px;
  }
  
  .upload-prompt p {
    color: #666;
    margin: 0;
  }
  
  .upload-progress {
    padding: 20px 0;
  }
  
  .progress-bar {
    height: 10px;
    background-color: #eee;
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 10px;
  }
  
  .progress-fill {
    height: 100%;
    background-color: #4caf50;
    transition: width 0.3s;
  }
  
  .upload-success {
    text-align: center;
  }
  
  .preview-image {
    max-width: 100%;
    max-height: 300px;
    border-radius: 4px;
    margin-bottom: 10px;
    border: 1px solid #eee;
  }
  
  .image-info {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 4px;
    text-align: left;
    display: inline-block;
  }
  
  .image-info p {
    margin: 5px 0;
    font-size: 14px;
  }
  
  .upload-options {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
    flex: 1;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 14px;
  }
  
  .form-group select, .form-group input[type="url"] {
    width: 100%;
    padding: 8px 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .form-group input[type="range"] {
    width: 100%;
  }
  
  .error-message {
    color: #f44336;
    padding: 10px;
    background-color: #ffebee;
    border-radius: 4px;
    margin-top: 10px;
  }
  
  .success-message {
    color: #4caf50;
    padding: 10px;
    background-color: #e8f5e9;
    border-radius: 4px;
    margin-top: 10px;
  }
  
  /* URL upload section */
  .upload-button, .retrieve-button {
    background-color: #2196f3;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
    margin-bottom: 20px;
  }
  
  .upload-button:hover, .retrieve-button:hover {
    background-color: #0b7dda;
  }
  
  .upload-button:disabled, .retrieve-button:disabled {
    background-color: #9e9e9e;
    cursor: not-allowed;
  }
  
  /* Retrieve section */
  .retrieve-options {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .retrieve-result {
    margin-top: 20px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 4px;
    border: 1px solid #eee;
  }
  
  .blob-info, .data-url-info {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 15px;
  }
  
  .view-blob-button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    margin-top: 10px;
  }
  
  .view-blob-button:hover {
    background-color: #45a049;
  }
  
  .truncated-data-url {
    background-color: #eee;
    padding: 10px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 10px;
  }
  
  /* Delete section */
  .current-images {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .image-type-card {
    border: 1px solid #eee;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .image-type-card h4 {
    padding: 10px 15px;
    margin: 0;
    background-color: #f5f5f5;
    border-bottom: 1px solid #eee;
  }
  
  .image-container {
    position: relative;
    height: 200px;
    overflow: hidden;
  }
  
  .type-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity 0.3s;
  }
  
  .image-container:hover .image-overlay {
    opacity: 1;
  }
  
  .delete-button {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }
  
  .delete-button:hover {
    background-color: #d32f2f;
  }
  
  .no-image {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    color: #999;
  }
  
  .image-loading {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    color: #666;
  }
  
  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Capabilities section */
  .capability-card {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .capability-status {
    display: flex;
    align-items: center;
    margin: 15px 0;
  }
  
  .checking {
    color: #ff9800;
  }
  
  .supported, .not-supported {
    display: flex;
    align-items: center;
    font-weight: bold;
  }
  
  .supported {
    color: #4caf50;
  }
  
  .supported svg {
    fill: #4caf50;
    margin-right: 5px;
  }
  
  .not-supported {
    color: #f44336;
  }
  
  .not-supported svg {
    fill: #f44336;
    margin-right: 5px;
  }
  
  .capability-description {
    color: #666;
    font-size: 14px;
    line-height: 1.5;
  }
  
  .server-config {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .server-config table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .server-config td {
    padding: 8px;
    border-bottom: 1px solid #eee;
  }
  
  .server-config tr:last-child td {
    border-bottom: none;
  }
  
  .server-config td:first-child {
    font-weight: bold;
    width: 40%;
  }
  </style>