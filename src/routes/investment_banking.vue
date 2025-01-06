<template>
    <Nav_Bar></Nav_Bar>
    <Currencies_Trend style="margin-top: 100px"></Currencies_Trend>
    <h1 style="color: gold; padding-left: 20px;">Investment Banking</h1>
    <div style="background-color: aqua; height: 2px; width: 85%; margin: 10px 0px 20px 20px;">.</div>
    <div class="video-section">
      <video autoplay muted loop playsinline>
        <source src="../assets/videos/investment.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
    <div class="content-section">
        <h1>Why Open an Investment Banking Account?</h1>
<p>
  An investment banking account provides access to specialized financial services for businesses and individuals looking to manage assets, raise capital, and pursue strategic growth opportunities. It is a crucial tool for complex financial transactions, tailored investment strategies, and achieving long-term goals.
</p>
<h2>Benefits of an Investment Banking Account</h2>
<ul>
  <li>Access to advisory services for mergers, acquisitions, and restructuring.</li>
  <li>Customized investment solutions to optimize portfolio performance.</li>
  <li>Support in raising capital through equity, debt, or hybrid instruments.</li>
  <li>Management of large-scale financial transactions with precision and expertise.</li>
  <li>Comprehensive market research and strategic guidance.</li>
</ul>
<h2>Driving Strategic Growth</h2>
<p>
  An investment banking account offers unparalleled resources for capital market access, financial advisory, and tailored solutions to meet unique investment goals. By partnering with investment banking services, businesses and individuals can unlock new growth opportunities, mitigate risks, and achieve financial success on a global scale.
</p>
      <router-link to="/new_account"><button>Invest</button></router-link>
    </div>
  </template>
  <script>
  import Nav_Bar from '../components/navbar.vue'
  import Currencies_Trend from '../components/exchange_r.vue'
      export default {
          name: 'Investment_Banking',
          emits: ['close'],
          data() {
              return {
                  data1: "Hello"
              }
          },
          components: {
            Nav_Bar,
            Currencies_Trend
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