<template>
  <div class="container" content="no-cache">
    <div v-if="loading" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i> Please wait a moment...
      <br>
      <br>
      <v-progress-circular color="green" indeterminate model-value="20" :size="47"></v-progress-circular>
    </div>
    <div class="comic-viewer" v-else-if="comics.length">
      <img :src="currentComic.img" :alt="currentComic.story" id="comic-image" @error="imageError" @load="imageLoaded">
      <p id="comic-story">{{ currentComic.story }}</p>
      <div class="button-container">
        <button @click="prevComic" id="prev-btn" :disabled="currentIndex === 0">
          <i class="fas fa-arrow-left"></i> Back
        </button>
        <button @click="nextComic" id="next-btn" :disabled="isNextDisabled">
          Next <i class="fas fa-arrow-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      comics: [],
      currentIndex: 0,
      loading: true,
      isNextDisabled: false,
      errorLoadingImage: false
    };
  },
  computed: {
    currentComic() {
      return this.comics[this.currentIndex];
    }
  },
  methods: {
    async loadComics() {
      const gifUrls = JSON.parse(localStorage.getItem('gifUrls')) || [];
      const stories = JSON.parse(localStorage.getItem('stories')) || [];

      if (gifUrls.length && stories.length) {
        this.comics = gifUrls.map((url, index) => ({
          img: url,
          story: stories[index]
        }));

        this.loading = false;
      } else {
        await new Promise(resolve => setTimeout(resolve, 3000)); // Simulate waiting for GIFs to be generated
        this.loadComics(); // Retry loading comics
      }
    },
    nextComic() {
      if (this.currentIndex < this.comics.length - 1) {
        this.currentIndex++;
        this.isNextDisabled = this.currentIndex === this.comics.length - 1;
      }
    },
    prevComic() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.isNextDisabled = false;
      }
    },
    imageError() {
      console.error('Error loading image.');
      this.errorLoadingImage = true;
      this.loading = false;
    },
    imageLoaded() {
      this.loading = false;
      this.errorLoadingImage = false;
    }
  },
  created() {
    this.loadComics();
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  flex-direction: column;
}

.loading-spinner {
  font-size: 1.5em;
  color: #42b983;
}

.comic-viewer {
  text-align: center;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

#comic-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

#comic-story {
  margin-top: 20px;
  font-size: 1.2em;
  color: #2c3e50;
}

.button-container {
  margin-top: 20px;
}

button {
  background-color: #42b983;
  border: none;
  color: white;
  padding: 10px 20px;
  font-size: 1em;
  cursor: pointer;
  border-radius: 4px;
  margin: 0 10px;
}

button:hover {
  background-color: #35495e;
}

button:disabled {
  background-color: #c0c0c0;
  cursor: not-allowed;
}
</style>
