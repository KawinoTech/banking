<template>
    <div class="container-lg">
      <div class="justify-content-center align-items-center">
        <div>
          <!-- Navigation Bar Contains GT Logo, Search bar, Notification icon, and profile picture update -->
          <nav
            class="navbar navbar-light fixed-top navbar-expand-xl mb-3"
            style="background-color: white;"
          >
            <!-- Logo -->
            <a href="#" class="navbar-brand mb-0 h1">
              <router-link to="/home">
                <img
                  src="../assets/logo.png"
                  alt="Logo"
                  width="30"
                  height="24"
                  class="d-inline-block align-text-top"
                />
              </router-link>
              Vue JS
            </a>
  
            <!-- Navbar toggle for smaller screens -->
            <button
              class="navbar-toggler"
              type="button"
              data-bs-target="#navbarNav"
              data-bs-toggle="collapse"
              aria-expanded="false"
              aria-controls="navbarNav"
              aria-label="Toggle navigation"
            >
              <span class="navbar-toggler-icon"></span>
            </button>
  
            <!-- Collapsible content -->
            <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav">
                <li class="nav-item active m-2">
                  <router-link
                    to="/customer_service"
                    style="text-decoration: none;"
                  >
                    <i class="fa-solid fa-circle-info"></i> Customer Care
                  </router-link>
                </li>
              </ul>
              <ul class="navbar-nav m-2">
                <li class="nav-item active">
                  <router-link
                    to="/report_problem"
                    style="text-decoration: none;"
                  >
                    <i
                      style="color: red"
                      class="fa-solid fa-circle-exclamation fa-beat"
                    ></i>
                    Report Problem
                  </router-link>
                </li>
              </ul>
              <ul class="navbar-nav">
                <li class="nav-item active m-2">
                    <i class="fa-solid fa-door-open"></i>
                  <button class="custom-button" @click="handleClick">
                    Log Out
                  </button>
                </li>
              </ul>
            </div>
          </nav>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "Nav_Bar",

    methods: {
      handleClick() {
      // Clear any authentication or session storage
      localStorage.removeItem("accessToken");
      localStorage.removeItem("expiresAt");
      sessionStorage.clear();

      // Redirect the user to the login page
      this.$router.push("/login")
      },
    },
  };
  </script>
  
  <style scoped>
  /* Icon Styling */
  i {
    margin-right: 5px;
    font-size: large;
    text-decoration: none;
  }
  
  /* Custom Button Styling */
  .custom-button {
    display: inline-block;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    color: rgba(0, 0, 0, 0.822);
    background-color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  
  .custom-button:hover {
    background-color: white;
    transform: scale(1.05);
  }
  
  .custom-button:active {
    background-color: white;
    transform: scale(1);
  }
  
  .custom-button:disabled {
    background-color: #d6d6d6;
    color: #8c8c8c;
    cursor: not-allowed;
    box-shadow: none;
  }
  </style>
  