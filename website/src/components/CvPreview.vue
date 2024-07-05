<template>
  <div class="image-container">
    <img
      v-if="imageSrc"
      :src="imageSrc"
      alt="Fetched Image"
      class="full-size-image"
    />
    <p v-else>Loading image...</p>
    <button @click="fetchPdf" class="download-button">Télécharger le CV</button>
    <button @click="GoToTrainings" class="download-button">Voir mes formations !</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      imageSrc: null,
    };
  },
  mounted() {
    this.fetchImage();
  },
  methods: {
    fetchImage() {
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
    GoToTrainings() {
      this.$router.push('/courses');
    },
    fetchPdf() {
      const pdfUrl = "http://127.0.0.1:5000/cv_download";

      fetch(pdfUrl)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.blob();
        })
        .then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.style.display = "none";
          a.href = url;
          a.download = "John_Doe_CV.pdf";
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
        })
        .catch((error) => {
          console.error("Error fetching PDF:", error);
        });
    },
  },
};
</script>

<style>
.image-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.full-size-image {
  max-width: 80%;
  max-height: 80%;
}

.download-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
