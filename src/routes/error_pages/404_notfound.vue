<template>
    <div class="container">
        <h1>404</h1>
        <p>Oops! The page you are looking for does not exist.</p>
        <div id="icon"><i class="fa-solid fa-circle-exclamation fa-beat-fade"></i></div>
        <a href="/">Go Back Home</a>
    </div>
</template>
<script>
export default {
    name: "Not_Found",
    data() {
        return {
            
        }
    }
}
</script>

<style scoped>
        .container {
            text-align: center;
        }
        h1 {
            font-size: 5rem;
            margin: 0;
            color: red;
        }
        p{
            font-size: 1.5rem;
            margin: 10px 0 20px;
            color: aqua;
        }
        a {
            text-decoration: none;
            color: white;
            background-color: gold;
            padding: 10px 20px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        a:hover {
            background-color: #0056b3;
        }

        i {
            color: red;
            font-size: 100px;
        }
        #icon {
            margin-bottom: 100px;
        }

</style>