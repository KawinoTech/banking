<template>
    <Nav_Bar></Nav_Bar>
    <h1 style="color: gold; margin-top: 100px; padding-left: 20px;">Corporate Banking</h1>
    <div style="background-color: aqua; height: 2px; width: 85%; margin: 10px 0px 20px 20px;">.</div>
    <div class="video-section">
      <video autoplay muted loop playsinline>
        <source src="../assets/videos/corporate.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
    <div class="content-section">
        <h1>Why Open a Corporate Account?</h1>
<p>
  A corporate account is a vital resource for businesses to efficiently manage their financial operations, 
  streamline transactions, and support growth. Whether you are a startup, SME, or large enterprise, 
  a corporate account offers tools designed to meet your unique business needs.
</p>
<h2>Benefits of a Corporate Account</h2>
<ul>
  <li>Facilitate high-volume transactions with ease and security.</li>
  <li>Access to advanced payment and collection systems, including bulk payments and direct debits.</li>
  <li>Overdraft and credit facilities to manage working capital effectively.</li>
  <li>Multi-user access and role-based permissions for better team management.</li>
  <li>Seamless integration with accounting software and digital banking platforms.</li>
</ul>
<h2>Empowering Business Growth</h2>
<p>
  A corporate account ensures that businesses have the flexibility and resources to scale operations, 
  manage cash flow, and make informed financial decisions. It’s a strategic tool to help 
  businesses achieve their goals and thrive in a competitive market.
</p>

      <router-link to="/new_account"><button>Open Account</button></router-link>
    </div>
  </template>
  <script>
  import Nav_Bar from '../components/navbar.vue'
      export default {
          name: 'Corporate_Account',
          emits: ['close'],
          data() {
              return {
                  data1: "Hello"
              }
          },
          components: {
            Nav_Bar
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