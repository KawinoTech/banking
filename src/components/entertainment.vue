<template>
    <div class="container">
        <div class="card" style="width: 16rem;">
            <img src="../assets/images/ufc.jpg" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">UFC</h5>
                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                <button type="button" class="btn btn-success">Personal</button>
            </div>
        </div>
        <div class="card" style="width: 16rem;">
            <img src="../assets/images/avengers.jpg" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">Movies & TV Shows</h5>
                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                <button type="button" class="btn btn-success">Personal</button>
            </div>
        </div>
        <div class="card" style="width: 16rem;">
            <img src="../assets/images/matchday.jpg" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">NFL</h5>
                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                <button type="button" class="btn btn-success">Personal</button>
            </div>
        </div>
    </div>
    <Premier_League></Premier_League>
</template>
<script>
import Premier_League from '../components/premierleague.vue'
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
    font-size: medium;
    color: white;
}
p {
    color: aqua;
}
.card {
    background: none;
    border: none;
}
.btn {
    background: gold;
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