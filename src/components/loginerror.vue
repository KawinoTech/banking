<template>
    <div class="message_area">
    <p>Invalid Credentials</p>
    </div>
<section>
  <div class="container">
    <div class="circle">
      <!-- You can place your icon or content inside this div -->
      <div class="icon">
        <!-- Your icon goes here -->
        <i class="fa-solid fa-xmark fa-shake"></i>
      </div>
    </div>
  </div>
</section>
<div class="button_area" style="margin: 30px;">
<router-link to="/login"><button type="button" class="btn btn-success">Try Again</button></router-link>
</div>
</template>
<script>
export default {
    name: "Login_Error_Pg",
    data() {
        return {
            
        }
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
  color: red;
}
p {
    color: red;
    width: 100%;
  display: flex;
  justify-content: center;
}
button {
    margin: 20px;
}

</style>