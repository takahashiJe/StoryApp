<template>
  <div id="app">
    <nav>
      <router-link to="/">Generate</router-link>
      <router-link to="/story">Story</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #42b983;
  text-decoration: none;
  padding: 0 15px;
}

nav a.router-link-exact-active {
  color: #35495e;
}
</style>
