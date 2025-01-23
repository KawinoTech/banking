<template>
    <div class="container">
        <div class="card" style="width: 16rem;">
            <img src="../../assets/images/ufc.jpg" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">UFC</h5>
                <p class="card-text">Catch the UFC action live and never miss a moment of the excitement, goals, and drama!</p>
                <a href="https://www.espn.com/mma/schedule/_/league/ufc"><button type="button" class="btn btn-success">Pay Per View</button></a>
            </div>
        </div>
        <div class="card" style="width: 16rem;">
            <img src="../../assets/images/avengers.jpg" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">Movies & TV Shows</h5>
                <p class="card-text">Check out Netflix movies and TV-Shows</p>
                <a href="https://www.netflix.com/ke/"><button type="button" class="btn btn-success">Stream</button></a>
            </div>
        </div>
        <div class="card" style="width: 16rem;">
            <img src="../../assets/images/matchday.jpg" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">NFL</h5>
                <p class="card-text">Catch the NFL action live and never miss a moment of the excitement, goals, and drama!</p>
                <a href="https://www.dazn.com/en-KE/l/nfl-game-pass"><button type="button" class="btn btn-success">Purchase ticket</button></a>
            </div>
        </div>
    </div>
    <Premier_League></Premier_League>
</template>
<script>
import Premier_League from './premierleague.vue'
export default {
    name: 'Enter_tainment',
    components: {
        Premier_League
    }
  };
</script>
<style scoped>
.container {
    height: auto;
    width: 100%;
    display: flex;
    flex-wrap: wrap; /* Allow elements to wrap to the next row */
    justify-content: space-between;
    margin: 20px;
}

h5 {
    font-size: larger;
    color: gold;
}
p {
    color: aqua;
}
.card {
    background: none;
    border: none;
}
.btn {
    background: rgb(0, 119, 255);
    color: white;
    border: 0;
}
.container > div {
    flex: 1 1 calc(33.33% - 20px); /* Adjust each item's width */
    margin: 10px; /* Spacing between items */
}
@media (max-width: 768px) {
    .container > div {
        flex: 1 1 100%; /* Make items take the full width on small screens */
    }
}
</style>