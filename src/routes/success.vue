<template>
    <div class="message_area">
    <p>Congratulations, The Process was a Success</p>
    </div>
<section>
  <div class="container">
    <div class="circle">
      <!-- You can place your icon or content inside this div -->
      <div class="icon">
        <!-- Your icon goes here -->
        <i class="fa-solid fa-check fa-beat"></i>
      </div>
    </div>
  </div>
</section>
<div class="button_area" style="margin: 30px;">
<router-link to="/home"><button type="button" class="btn btn-success">Return Home</button></router-link>
</div>
<Footer></Footer>
</template>
<script>
import Footer from '@/components/others/footer.vue';
export default {
    name: "Success_Pg",
    components: {
      Footer
    }
}
</script>

<style scoped>
section, .message_area, .button_area {
  height: 100%;
  margin: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.circle {
  width: 200px;
  height: 200px;
  border: 2px solid white; /* Adjust the border thickness as needed */
  border-radius: 50%; /* Makes the square div a circle */
  display: flex;
  justify-content: center;
  align-items: center;
}

.icon {
  font-size: 70px; /* Adjust icon size as needed */
  color: green;
}
p {
    color: aqua;
    width: 100%;
  display: flex;
  justify-content: center;
}
</style>