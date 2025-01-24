<template>
  <!-- Navigation bar -->
  <Nav_Bar></Nav_Bar>

  <h3>Close Account</h3>

  <!-- Accordion to display accounts -->
  <div class="accordion" id="accordionExample">
    <div
      class="accordion-item"
      v-for="(account, index) in all_accounts"
      :key="index"
    >
      <h2 :id="'heading' + index" class="accordion-header">
        <button
          class="accordion-button"
          type="button"
          :data-bs-toggle="'collapse'"
          :data-bs-target="'#collapse' + index"
          aria-expanded="index === 0"
          :aria-controls="'collapse' + index"
        >
          <strong>{{ account.account_type }}</strong>: {{ account.account_no || `Accordion Item #${index + 1}` }}
        </button>
      </h2>

      <div
        :id="'collapse' + index"
        class="accordion-collapse collapse"
        :class="{ show: index === 0 }"
        :aria-labelledby="'heading' + index"
        data-bs-parent="#accordionExample"
      >
        <div class="accordion-body">
          <strong>{{ account.account_no || 'Account' }}</strong>
          <p>Balance: {{ account.account_balance }}</p>
          <p>Account Number: {{ account.account_no }}</p>
        </div>

        <!-- Button to trigger account closure -->
        <button
          class="btn-close-account"
          @click="showConfirmation(account.account_no, account.account_balance)"
        >
          Close Account
        </button>
      </div>
    </div>
  </div>

  <!-- Modal for failure scenario (when the account balance is not zero) -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h2>Sorry Customer</h2>
      <p class="modal-text">
        We could not proceed with your request. Please withdraw all funds from this account before attempting to close it.
      </p>
      <p class="modal-text">
        If you have any questions, contact our support team at 
        <a href="mailto:support@example.com">support@example.com</a> or call us at 
        <a href="tel:+123456789">+1 (234) 567-89</a>.
      </p>
      <p class="modal-text">
        Our operating hours are Monday to Friday, 9 AM to 6 PM.
      </p>
      <button @click="showModal = false" class="btnclose">
        Close
      </button>
    </div>
  </div>

  <!-- Confirmation modal for account closure -->
  <div class="modal-overlay" v-if="isConfirmationVisible">
    <div class="modal-card-">
      <h2 class="modal-title-">Confirm Details</h2>
      <p class="modal-content-">Dear Customer, we regret to see you leaving</p>

      <div v-if="!isProcessing" class="modal-buttons-">
        <button class="modal-btn- confirm" @click="confirmTransfer(accountNo, accountBalance)">Yes</button>
        <button class="modal-btn- cancel" @click="cancelTransfer">Cancel</button>
      </div>

      <div v-if="isProcessing">
        <p class="wait">Processing<i class="fa-regular wait fa-clock fa-spin"></i></p>
      </div>
    </div>
  </div>
</template>


<script>
import Nav_Bar from "../../components/navbar.vue";

export default {
  name: "Account_Closure",
  data() {
    return {
      all_accounts: [], // Stores all user accounts
      showModal: false, // Controls the display of the error modal
      isConfirmationVisible: false, // Controls the visibility of the confirmation modal
      isProcessing: false, // Controls the display of a loading spinner during the closure process
      accountNo: "", // The account number selected for closure
      accountBalance: "", // The balance of the selected account
    };
  },
  components: {
    Nav_Bar, // Navigation bar component
  },
  mounted() {
    this.fetchData(); // Fetch accounts data when the component is mounted
  },
  methods: {
    // Fetches all accounts for the logged-in user
    async fetchData() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/post/get_user_transactive_accounts",
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const data = await response.json();
        this.all_accounts = data; // Store the fetched accounts
      } catch (error) {
        console.error("Error fetching data:", error); // Log any error during fetch
      }
    },
    // Makes an API call to close the account
    async closeAccount(accountNo) {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/post/close_account/${accountNo}`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );
        if (response.ok) {
          setTimeout(() => this.$router.push('/success'), 2000); // Redirect to success page after closure
          this.fetchData(); // Refresh the list of accounts
        } else {
          alert("Failed to close account. Please try again.");
        }
      } catch (error) {
        setTimeout(() => this.$router.push('/failed'), 500); // Redirect to failed page on error
        console.error("Error closing account:", error); // Log any error during account closure
      }
    },
    // Shows the confirmation modal when trying to close an account
    showConfirmation(accountNo, accountBalance) {
      this.accountNo = accountNo; // Set the selected account number
      this.accountBalance = accountBalance; // Set the selected account balance
      this.isConfirmationVisible = true; // Show the confirmation modal
    },
    // Handles the account closure after confirmation
    confirmTransfer(accountNo, accountBalance) {
      if (accountBalance !== 0) {
        this.isConfirmationVisible = false; // Close the confirmation modal
        this.showModal = true; // Show the error modal
        return;
      }
      this.closeAccount(accountNo); // Close the account
      this.isProcessing = true; // Show the processing spinner
    },
    // Cancels the account closure and hides the confirmation modal
    cancelTransfer() {
      this.isConfirmationVisible = false;
    },
  },
};
</script>


<style>
/* Add your styles for the button here */
.btn-close-account {
  background-color: #dc3545; /* Bootstrap danger color */
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  margin-left: 20px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.btn-close-account:hover {
  background-color: #c82333; /* Darker red for hover */
}

.heading {
    text-decoration: underline;
}
.container {
    margin: 10px 20px 10px 20px;
}
span {
  font-size: small;
}
.accordion {
  margin-top: 20px;
  width: 75%;
}
.accordion-item {
  background-color: rgb(0, 19, 31);
  color: aqua;
}
h3 {
  color: gold;
  margin-top: 80px;
}


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6); /* Semi-transparent background for blur effect */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px); /* Applies blur to the background */
}

/* Modal content */
.modal-content {
  background-color: rgb(0, 19, 31);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 500px;
  width: 100%;
  animation: fadeIn 0.3s ease;
}

/* Heading styling */
.modal-content h2 {
  color: #dc3545; /* Bootstrap danger color */
  margin-bottom: 1rem;
}

/* Close button */
.btnclose {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
  margin-top: 1rem;
}

.btnclose:hover {
  background-color: #b52b3b;
}
.modal-text {
  color: aqua;
}
/* Responsive animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>