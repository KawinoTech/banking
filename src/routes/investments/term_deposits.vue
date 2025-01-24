<template>
    <Nav_Bar></Nav_Bar>
    <h1>Term Deposit</h1>
    <form action="#">
      <div class="form-group">
        <label for="account" class="form-label">Choose Account</label>
        <select
          v-model="formData.account"
          id="account"
          name="account"
          class="form-select"
          style="background-color: rgb(0, 19, 31); color: white; width: 50%;"
        >
          <option selected>Select Account to debit</option>
          <option
            v-for="account in all_accounts"
            :key="account.account_no"
          >{{ account.account_type }} {{ account.currency }}:{{ account.account_no }}</option>
        </select>
      </div>
  
      <div class="form-group">
        <p v-if="balance > 0 && formData.amount !== ''" class="within_limit">
          Balance: {{ balance }}
        </p>
        <p v-else-if="balance < 0 && formData.amount !== ''" class="exceed_limit">
          Balance: {{ balance }}, Sorry! Insufficient Funds
        </p>
        <input
          type="text"
          id="amount"
          name="amount"
          v-model="formData.amount"
          placeholder="Enter Amount"
          @input="check_balance"
        />
      </div>
  
  
      <label for="tenure">Tenure (Month/s)</label>
      <input v-model="formData.tenure" type="number" id="tenure" name="tenure" placeholder="Enter tenure in months" required>
      <div>
        <p class="rate">Rate fixed at {{ this.interestRate }}</p>
      </div>
      <div class="form-group">
        <label for="account" class="form-label">Enter your PIN</label>
        <input
          v-model="formData.password"
          type="password"
          id="password"
          name="password"
          placeholder="PIN"
          style="background-color: rgb(0, 19, 31); border: none; border-bottom: 1px solid aqua; width: 25%;"
        />
      </div>
  
      <button type="button" class="btn btn-success" @click="showConfirmation">
        Book Term Deposit
      </button>
    </form>
    <div class="modal-overlay" v-if="isConfirmationVisible">
        <div class="modal-card-">
          <h2 class="modal-title-">Confirm Details</h2>
          <p class="modal-content-">
            Account Number: <span>{{ formData.account }}</span>
          </p>
          <p class="modal-content-">
            Tenure: <span>{{ formData.tenure }} months</span>
          </p>
          <p class="modal-content-">
            Amount: <span>{{ formData.amount }}</span>
          </p>
          <p class="modal-content-">
            Fixed Rate: <span>{{ this.interestRate }}</span>
          </p>
          <p class="modal-content-">
            Potential Interest: <span>{{ potentialInterest }}</span>
          </p>
          <div v-if="!isProcessing" class="modal-buttons-">
            <button class="modal-btn- confirm" @click="confirmTransfer">Yes</button>
            <button class="modal-btn- cancel" @click="cancelTransfer">Cancel</button>
          </div>
          <div>

          </div>
          <div v-if="isProcessing">
            <p class="wait">
              Processing<i class="fa-regular wait fa-clock fa-spin"></i>
            </p>
          </div>
        </div>
      </div>
  </template>
  
  <script>
  // URL for fetching user account data
  const url2 = "http://127.0.0.1:8000/post/get_user_transactive_accounts";
  
  // Import necessary utility functions and components
  import utils from "../../utils/utils";
  import Nav_Bar from "../../components/navbar.vue";

  export default {
    name: "Term_Deposit", // Component name
    components: {
      Nav_Bar // Navigation bar component
    },

    // Computed property to calculate potential interest for a term deposit
    computed: {
      potentialInterest() {
        return (Number(this.formData.amount) * Math.pow(1 + this.interestRate / 100, this.formData.tenure));
      }
    },

    data() {
      return {
        // Form data to hold user input values
        formData: {
          amount: "", // Amount to invest
          tenure: "", // Tenure for the deposit (in years/months)
          account: "", // Account from which the investment will be made
          password: "", // User password for validation (if necessary)
        },

        all_accounts: [], // List of all user accounts
        balance: "", // Balance after checking the available funds for the deposit
        isConfirmationVisible: false, // Flag to show confirmation modal
        isProcessing: false, // Flag to show processing state (for spinner or progress indication)
        interestRate: 4.453 // Default interest rate for the term deposit
      };
    },

    mounted() {
      this.fetchData(); // Fetch user account data when the component is mounted
    },

    methods: {
      // Helper method to find and return the substring after a specified character in a string
      findAndReturnSubsequent(str, char) {
        const index = str.indexOf(char);
        return index !== -1 && index < str.length - 1
          ? str.substring(index + 1)
          : ""; // Return substring after character if it exists, else return empty string
      },

      // Method to check if the balance is sufficient for the term deposit
      check_balance() {
        if (this.formData.account !== "" && this.formData.amount !== "") {
          for (const account of this.all_accounts) {
            if (this.findAndReturnSubsequent(this.formData.account, ":") === account.account_no) {
              this.balance = account.account_balance - this.formData.amount; // Calculate the remaining balance
            }
          }
        }
      },

      // Method to confirm the term deposit creation
      confirmTransfer() {
        this.bookTermDeposit(); // Call method to book the term deposit
        this.isProcessing = true; // Set processing state to true (e.g., show a spinner)
      },

      // Method to cancel the term deposit creation
      cancelTransfer() {
        this.isConfirmationVisible = false; // Hide the confirmation modal
      },

      // Method to show the confirmation modal after validating the input
      showConfirmation() {
        // Validate if any fields are empty
        if (utils.checkEmptyValues(this.formData)) {
          alert('Please fill in all required fields.'); // Show alert if any fields are empty
          return;
        }
        this.isConfirmationVisible = true; // Show the confirmation modal
      },

      // Method to book the term deposit with the provided details
      async bookTermDeposit() {
        try {
          // Validate if any fields are empty before proceeding
          if (utils.checkEmptyValues(this.formData)) {
            throw new Error("Empty Fields");
          }

          // Generate the HMAC signature for the request body (used for authentication)
          const requestBody = utils.generateHmacSignature({
            "amount": Number(this.formData.amount), // Convert amount to a number
            "maturity_period": this.formData.tenure, // The tenure (duration) of the deposit
            "account": this.findAndReturnSubsequent(this.formData.account, ":") // Extract account number
          });

          // Make the API request to book the term deposit
          const response = await fetch("http://127.0.0.1:8000/post/book_td", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`, // Pass access token in headers
            },
            body: JSON.stringify(requestBody), // Send the signed request body
          });

          // Check if the request was successful
          if (!response.ok) {
            throw new Error("Failed to post data");
          }

          // If successful, redirect to the success page
          setTimeout(() => {
            this.$router.push("/success");
          }, 2000);
        } catch (error) {
          // Handle any errors during the API call
          console.error("Error posting data:", error);
          setTimeout(() => {
            this.$router.push("/failed"); // Redirect to failed page in case of error
          }, 2000);
        }
      },

      // Method to fetch the user's account data
      async fetchData() {
        try {
          const response = await fetch(url2, {
            method: "GET",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`, // Pass access token in headers
            },
          });

          const data = await response.json();
          this.all_accounts.push(...data); // Add fetched accounts to the list
          this.loading = false; // Set loading to false when data is loaded
        } catch (error) {
          console.error("Error fetching data:", error); // Log any errors during data fetching
        }
      },
    },
  };
</script>

  
  <style scoped>
  h1 {
    color: gold;
    margin-left: 5px;
    margin-top: 80px;
  }
  .within_limit {
    margin-top: 10px;
    color: green;
  }
  .exceed_limit {
    margin-top: 10px;
    color: red;
  }
  label {
    color: antiquewhite;
    margin-left: 10px;
  }
  
  span {
    color: green;
  }
  form {
    margin-left: 10px;
  }
  #tenure {
    width: 25%;
    background-color: black;
    padding: 10px;
      margin: 10px 0;
      border: 1px solid aqua;
      border-radius: 5px;
      color: white;
  }
  .rate {
    color: gold;
    padding: 15px;
  }
  </style>
  