<template>
  <Nav_Bar></Nav_Bar>
  <h1 style="color: gold; margin-top: 100px; padding-left: 20px;">Savings Account</h1>
  <div style="background-color: aqua; height: 2px; width: 85%; margin: 10px 0px 20px 20px;">.</div>
  <div class="video-section">
    <video autoplay muted loop playsinline>
      <source src="../../assets/videos/savings.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
  </div>
  <div class="content-section">
    <h1>Why Open a Savings Account?</h1>
    <p>
      A savings account is one of the simplest ways to manage your finances, save for future needs, 
      and access funds when required. It provides security and liquidity while earning interest 
      on your deposited money.
    </p>
    <h2>Benefits of a Savings Account</h2>
    <ul>
      <li>Earn interest on your savings.</li>
      <li>Access to funds anytime, anywhere.</li>
      <li>Secure your money with FDIC-insured accounts (subject to country regulations).</li>
      <li>Enjoy online and mobile banking convenience.</li>
    </ul>
    <h2>The Future Value of Savings</h2>
    <p>
      Saving regularly builds financial discipline and ensures you're prepared for life's milestones. 
      Whether it's for retirement, education, or emergencies, a savings account helps secure your 
      future and turn dreams into reality.
    </p>
    <router-link to="/new_account"><button>Open Account</button></router-link>
  </div>
  <Footer></Footer>
</template>
<script>
import Footer from '@/components/others/footer.vue';
import Nav_Bar from '../../components/navbar.vue'
    export default {
        name: 'Savings_Account',
        emits: ['close'],
        data() {
            return {
                data1: "Hello"
            }
        },
        components: {
          Nav_Bar, Footer
}
    }
</script>
<style scoped>

.video-section {
  width: 90%; /* Takes up 80% of the screen width */
  margin: 0 auto; /* Centers the video horizontally */
}

.video-section video {
  width: 100%; /* Ensures the video fills the video section */
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.content-section {
  width: 80%; /* Matches the width of the video section */
  margin: 20px auto; /* Centers the content and adds space above it */
  padding: 20px;
  background-color: none;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1, h2 {
  color: white;
}

p {
  font-size: 16px;
  line-height: 1.6;
  color: aqua;
}

ul {
  list-style: disc;
  padding-left: 20px;
  color: green;
}

li {
  font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 10px 0;
}
button {
  margin-top: 15px;
  padding: 10px 15px;
  font-size: 16px;
  color: #fff;
  background-color: gold;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 150px;
}

button:hover {
  background-color: #218838;
}
</style>