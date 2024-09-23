<template>
        <div class="container-lg">
            <div class="justify-content-center align-items-center">
                <div>
                    <!--Navigation Bar Contains GT Logo, Search bar, Notification icon and profile picture update-->
                    <nav class="navbar navbar-light fixed-top navbar-expand-xl mb-3" style="background-color: white;">
                        <a href="#" class="navbar-brand mb-0 h1">
 <router-link to="/home"><img src="./assets/logo.png" alt="Logo" width="30" height="24" class="d-inline-block align-text-top"></router-link>
                            Vue JS
                        </a>
                        <!-- Toggles the navbar when screen size reduces
                        data-bs-toggle - invokes the navbar when button is pressed
                        data-bs-target - targets the navbar specified by its id -->
                        <button class="navbar-toggler" type="button" data-bs-target="#navbarNav" 
                        data-bs-toggle="collapse" aria-expanded="false" aria-controls="navbarNav" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul class="navbar-nav">
                                <li class="nav-item active m-2">
                                    <a href="#" class="nav-link"><i class="fa-solid fa-plus"></i>Add Idea</a>
                                </li>
                            </ul>
                            <ul class="navbar-nav">
                                <li class="nav-item active m-2">
                                    <a href="#" class="nav-link"><i class="fa-solid fa-square-share-nodes"></i>Lobby Idea</a>
                                </li>
                            </ul>
                            <ul class="navbar-nav m-2">
                                <li class="nav-item active">
                                    <a href="#" class="nav-link"><i class="fa-solid fa-list-ol"></i>Rankings</a>
                                </li>
                            </ul>
                            <ul class="navbar-nav m-2">
                                <li class="nav-item active">
                                    <a href="#" class="nav-link"><i class="fa-solid fa-ranking-star"></i>Top Tier</a>
                                </li>
                            </ul>
                            <ul class="navbar-nav m-2">
                                <li class="nav-item active">
                                    <a href="#" class="nav-link"><i class="fa-solid fa-magnifying-glass"></i>The Lobby</a>
                                </li>
                            </ul>
                            <ul class="navbar-nav m-2">
                                <li class="nav-item active">
                                    <a href="#" class="nav-link"><i class="fa-solid fa-person-through-window"></i>Logout</a>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
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