<template>
    <div class="carousel">
      <div class="carousel-slides" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
        <img v-for="(image, index) in images" :key="index" :src="image" alt="Slide image" />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      images: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        currentIndex: 0,
      };
    },
    computed: {
      imageCount() {
        return this.images.length;
      },
    },
    methods: {
      nextSlide() {
        this.currentIndex = (this.currentIndex + 1) % this.imageCount;
      },
      prevSlide() {
        this.currentIndex =
          (this.currentIndex - 1 + this.imageCount) % this.imageCount;
      },
    },
    mounted() {
      setInterval(() => {
        this.nextSlide();
      }, 3000); // Change slide every 3 seconds
    },
  };
  </script>
  
  <style scoped>
  .carousel {
    overflow: hidden;
    width: 100%;
    height: 450px;
    position: relative;
    display: block;
  }
  
  .carousel-slides {
    display: flex;
    transition: transform 0.5s ease-in-out;
  }
  
  .carousel-slides img {
    width: 100%;
    height: 350px;
    flex-shrink: 0;
  }
  
  .controls {
    position: absolute;
    top: 50%;
    width: 100%;
    display: flex;
    justify-content: space-between;
    transform: translateY(-50%);
  }
  
  .controls button {
    background: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    padding: 10px;
    cursor: pointer;
  }
  @media (max-width: 768px) {
    .carousel {
      display: none; /* Hides the carousel */
    }
  }
</style>