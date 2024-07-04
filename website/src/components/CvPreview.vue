<template>
  <div class="image-container">
    <img
      v-if="imageSrc"
      :src="imageSrc"
      alt="Fetched Image"
      class="full-size-image"
    />
    <p v-else>Loading image...</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      imageSrc: null, // URL or base64 string of the image
    };
  },
  mounted() {
    this.fetchImage();
  },
  methods: {
    fetchImage() {
      // Replace with your API endpoint or image URL
      const imageUrl = "http://127.0.0.1:5000/cv";

      fetch(imageUrl)
        .then((response) => response.blob())
        .then((blob) => {
          this.imageSrc = URL.createObjectURL(blob);
        })
        .catch((error) => {
          console.error("Error fetching image:", error);
        });
    },
  },
};
</script>

<style>
.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.full-size-image {
  max-width: 100%;
  max-height: 100%;
}
</style>
