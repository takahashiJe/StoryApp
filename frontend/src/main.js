import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

loadFonts()

createApp(App)
  .use(router)
  .use(store)
  .use(vuetify)
  .mount('#app')

// import Vue from 'vue';
// import App from './App.vue';
// import '@fortawesome/fontawesome-free/css/all.css';
// import '@fortawesome/fontawesome-free/js/all.js';

// Vue.config.productionTip = false;

// new Vue({
//   render: h => h(App),
// }).$mount('#app');
