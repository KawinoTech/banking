<template>
    <!-- Navigation bar -->
    <Nav_Bar></Nav_Bar>
  
    <h3>Coming Soon</h3>
  
  </template>
  
  
  <script>
  import Nav_Bar from "../../components/navbar.vue";
  
  export default {
    name: "Financial_Markets",
    components: {Nav_Bar}

  };
  </script>

  
  <style>
  h3 {
    text-align: center;
    color: gold;
    font-size: 100px;
  }
  </style>