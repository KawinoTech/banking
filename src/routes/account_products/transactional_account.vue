<template>
    <Nav_Bar></Nav_Bar>
    <h1 style="color: gold; margin-top: 100px; padding-left: 20px;">Transactional Account</h1>
    <div style="background-color: aqua; height: 2px; width: 85%; margin: 10px 0px 20px 20px;">.</div>
    <div class="video-section">
      <video autoplay muted loop playsinline>
        <source src="../../assets/videos/transactional.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
    <div class="content-section">
      <h1>Why Open a Transactional Account?</h1>
<p>
  A transactional account, commonly known as a current account, is an essential tool for managing 
  day-to-day finances and facilitating smooth financial transactions. It offers quick access to funds 
  and supports high levels of financial activity for both individuals and businesses.
</p>
<h2>Benefits of a Transactional Account</h2>
<ul>
  <li>Seamless deposits and withdrawals, including ATM access.</li>
  <li>Unlimited transactions with no minimum holding period.</li>
  <li>Access to overdraft facilities for additional financial flexibility.</li>
  <li>Integration with digital banking platforms for online payments and transfers.</li>
</ul>
<h2>Enhancing Financial Management</h2>
<p>
  A transactional account ensures that you can efficiently manage cash flow, settle bills, and meet 
  daily financial obligations. It's a cornerstone for organizing your finances and achieving 
  both personal and business goals with ease.
</p>

      <router-link to="/new_account"><button>Open Account</button></router-link>
    </div>
    <Footer></Footer>
  </template>
  <script>
  import Footer from '@/components/others/footer.vue';
  import Nav_Bar from '../../components/navbar.vue'
      export default {
          name: 'Transactional_Account',
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