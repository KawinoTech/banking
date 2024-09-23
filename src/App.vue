<template>
  <nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <router-link to="/home"><img src="./assets/logo.png" alt="Logo" width="30" height="24" class="d-inline-block align-text-top"></router-link>
        Vue JS Bank
      </a>
    </div>
  </nav>
  <router-view></router-view>
      <footer>
        <p style="font-size: 10px;">Copyright &copy; All rights reserved</p>
        <p v-bind:class="status" style="font-size: 10px;">Application built by Okoth Kawino</p>
    </footer>
</template>

<script>

export default {
  name: 'App',
  data(){
    return {
      status: 'danger',
      movie: '',
      showpop: false
    }
  }
}
</script>
<style scoped>

footer {
    display: block;
    color: aqua;
    text-align: center;
    padding: 20px 0;
    bottom: 0;
    width: 100%;
}
.danger {
  color: red;
}
.inp {
  color: white;
}
</style>