<template>
    <div class="notification" v-if="visible">
      <p>{{ message }}</p>
      <button @click="closeNotification">Close</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      message: {
        type: String,
        required: true,
        default: 'New Session.',
      },
    },
    data() {
      return {
        visible: true,
      };
    },
    methods: {
      closeNotification() {
        this.visible = false;
      },
    },
  };
  </script>
  
  <style scoped>
  .notification {
    position: fixed;
    top: 20px;
    left: 20px;
    background: #f8d7da;
    color: #721c24;
    padding: 1rem 1.5rem;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    z-index: 1000;
  }
  button {
    background: #721c24;
    color: #fff;
    border: none;
    padding: 0.5rem 1rem;
    margin-left: 10px;
    cursor: pointer;
    border-radius: 3px;
  }
  button:hover {
    background: #501414;
  }
  .notification {
  animation: fadeIn 0.5s ease-in, fadeOut 0.5s ease-out 10s forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeOut {
  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}

  </style>
  