<template>
  <nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <router-link to="/home"><img src="./assets/logo.png" alt="Logo" width="30" height="24" class="d-inline-block align-text-top"></router-link>
        Vue JS Bank
      </a>
    </div>
  </nav>
  <Currencies_Trend></Currencies_Trend>
  <router-view></router-view>
      <footer>
        <p style="font-size: 10px;">Copyright &copy; All rights reserved</p>
        <p style="font-size: 10px;">Application built by Okoth Kawino</p>
    </footer>
</template>

<script>
import Currencies_Trend from './components/exchange_r.vue'


export default {
  name: 'App',
  components: {
    Currencies_Trend
  },

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
</style>
