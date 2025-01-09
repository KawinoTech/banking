<template>
    <div class="container">
        <div class="card" style="width: 18rem;">
            <img src="../../assets/images/uber.png" class="card-img-top" alt="...">
            <div class="card-body">
                <button type="button" class="btn btn-success">Request ride</button>
            </div>
        </div>
        <div class="card" style="width: 18rem;">
            <img src="../../assets/images/bolt1.jpg" class="card-img-top" alt="...">
            <div class="card-body">
                <button type="button" class="btn btn-success">Request ride</button>
            </div>
        </div>
        <div class="card" style="width: 18rem;">
            <img src="../../assets/images/little.png" class="card-img-top" alt="...">
            <div class="card-body">
                <button type="button" class="btn btn-success">Request ride</button>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'Trans_port',
  };
</script>
<style scoped>
.container {
    height: auto;
    width: 100%;
    display: flex;
    flex-wrap: wrap; /* Allow elements to wrap to the next row */
    justify-content: space-between;
    margin-left: 2px;
    margin-right: 2px;
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
img {
    height: 250px;
    width: 250px;
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