<template>
    <div class="container">
        <div class="video-container">
            <video autoplay muted>
                <source src="../../assets/videos/epl.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <div class="text-container">
            <h1>Premier League</h1>
            <p>"Catch the Premier League action live and never miss a moment of the 
                excitement, goals, and drama!</p>
            <h1>News</h1>
            <div class="news_container">
                <div>
                    <img src="../../assets/images/bre-v-ars.webp" class="card-img-top" alt="...">
                </div>
                <div class="text-container">
                    <p>
                    Arsenal beat Brentford to close gap on leaders Liverpool
                    Goals from Jesus, Merino and Martinelli give Gunners 3-1 win as they 
                    reduce gap to six points at the top
                    
                    </p>
                    <a href="https://www.premierleague.com/"><button type="button" class="btn btn-success">Stream<i class="fa-regular fa-circle-play fa-beat"></i></button></a>
                </div>
            </div>
            
        </div>
    </div>
</template>
<script>
export default {
  name: 'Premier_League',

     data(){
        return {
            loading: true,
        };
     },
}
</script>
<style scoped>
.container {
    display: flex;
    flex-wrap: wrap; /* Allows wrapping for responsiveness */
    width: 100%;
    max-width: 1200px;
    margin: 20px auto; /* Center the container */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    background-color: none;
    overflow: hidden;
}

/* Left side - video */
.video-container {
    flex: 1 1 50%;
    background-color: #000; /* Video container background */
}

.video-container video {
    width: 100%;
    height: 100%;
    display: block; /* Remove unwanted margins */
}

/* Right side - text */
.text-container {
    flex: 1 1 50%;
    padding: 20px;
    box-sizing: border-box; /* Includes padding in width calculations */
}

.text-container h1 {
    font-size: 1.5em;
    color: gold;
    margin-bottom: 10px;
}

.text-container p {
    font-size: 0.9em;
    color: white;
    line-height: 1.5;
    text-align: justify;
}

/* Responsive design */
@media (max-width: 768px) {
    .container {
        flex-direction: column; /* Stack items vertically */
    }
    .video-container,
    .text-container {
        flex: 1 1 100%;
    }
}
.news_container {
    display: flex;
    flex-wrap: wrap; /* Allows wrapping for responsiveness */
    justify-content: space-between;
}
img {
    height: 200px;
    width: 200px;
}

.btn {
    background: rgb(0, 119, 255);
    color: white;
    border: 0;
}

i {
    margin-left: 20px;
}
</style>