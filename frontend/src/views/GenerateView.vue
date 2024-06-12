<template>
  <div class="generate-container" content="no-cache">
    <h1>Generate GIF 画像生成</h1>
    <v-form @submit.prevent="submitStories">
      <label for="storyCount">Number of stories:</label>
      <input type="number" v-model="storyCount" id="storyCount" min="1" @change="generateStories">

      <div v-for="(story, index) in stories" :key="index" class="story-input">
        <label :for="'story' + index">Story {{ index + 1 }}:</label>
        <textarea v-model="stories[index]" :id="'story' + index" rows="3" required></textarea>
      </div>
      <button type="submit">Generate GIF</button>
    </v-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      storyCount: 0,// ユーザーが入力する数字を保存
      stories: [
        /* 'Once upon a time, there was a grandfather and a grandmother',
        'Grandpa went to the mountains to mow the lawn',
        'Grandma went to the river to wash clothes',
        'When Grandma was making a choice, a big peach came down the river',
        '',
        '' */
      ],// 生成されたstoriesを保存
      generateCount: 0,
      gifUrls: [],
    };
  },
  methods: {
    // ユーザーが入力した数だけstoriesの要素を生成するメソッド
    generateStories() {
      this.stories = Array.from({ length: this.storyCount }, (_, index) => `Story ${index + 1}`);
    },
    async submitStories() {
      try {
        const payload = { stories: this.stories };
        console.log('Sending stories to backend:', payload);

        this.$router.push('/story'); // Navigate to the story view immediately

        const response = await fetch('https://ibera.cps.akita-pu.ac.jp/api/generate-gif', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          if (response.status === 404) {
            console.error('Endpoint not found:', response.url);
          } else {
            console.error('HTTP error:', response.status, response.statusText);
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }

       /*  this.gifUrls = [
          'https://localhost:/api/static/animation_0.gif',
          'https://localhost:8001/api/static/animation_1.gif',
          'https://localhost:8001/api/static/animation_2.gif',
          'https://localhost:8001/api/static/animation_3.gif',
          'https://localhost:8001/api/static/animation_4.gif'
        ]; */
        this.fetchGifUrls()

        // Save the gifUrls and stories to localStorage to be accessed by CmicView.vue
        localStorage.setItem('gifUrls', JSON.stringify(this.gifUrls));
        localStorage.setItem('stories', JSON.stringify(this.stories));

      } catch (error) {
        console.error('Error generating GIF:', error);
        alert(`Error generating GIF: ${error.message}`);
      }
    },
    fetchGifUrls() {
      this.gifUrls = this.getGifUrls();
    },
    getGifUrls() {
      let gifUrls = [];
      for(let step = 0; step < this.storyCount; step++){
        const url = "https://ibera.cps.akita-pu.ac.jp/api/static/animation_" + step + ".gif";
        gifUrls.push(url)
      }
      console.log(gifUrls)
      return gifUrls;
    }
  }
}
</script>

<style scoped>
.generate-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  padding: 20px;
  max-width: 800px;
  margin: 60px auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.story-input {
  margin-bottom: 20px;
  text-align: left;
}

.story-input label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #35495e;
}

.story-input textarea {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border-radius: 4px;
  border: 1px solid #dcdcdc;
  font-size: 1em;
  resize: none;
}

.story-input textarea:focus {
  outline: none;
  border-color: #42b983;
}

button {
  background-color: #42b983;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  font-size: 1em;
  margin-top: 20px;
}

button:hover {
  background-color: #35495e;
}

.gif-container {
  margin-top: 20px;
  text-align: center;
}

.gif-item {
  margin-bottom: 20px;
}

.gif-item img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}
</style>
