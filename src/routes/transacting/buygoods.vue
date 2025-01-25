<template>
  <div>
    <!-- Navigation bar -->
    <Nav_Bar></Nav_Bar>

    <!-- Buy Goods Form -->
    <form action="#">
      <h1>Buy Goods</h1>

      <!-- Account Selection -->
      <div class="form-group">
        <label for="account" class="form-label">Select Account to Debit</label>
        <select
          v-model="formData.account"
          id="account"
          name="account"
          class="form-select"
          style="background-color: rgb(0, 19, 31); color: white; width: 50%;"
        >
          <option v-for="account in all_accounts" :key="account.account_no">
            {{ account.account_type }} {{ account.currency }}:{{ account.account_no }}
          </option>
        </select>
      </div>

      <!-- Store Number Input -->
      <div class="form-group">
        <input
          v-model="formData.beneficiary"
          type="text"
          id="beneficiary"
          name="beneficiary"
          placeholder="Store Number"
        />
      </div>

      <!-- Amount Input -->
      <div class="form-group">
        <p
          v-if="balance > 0 && formData.amount != ''"
          class="within_limit"
        >
          Balance: {{ balance }}
        </p>
        <div
          class="overdraft"
          v-else-if="balance < 0 && formData.amount != ''"
        >
          <p class="exceed_limit">
            Balance: {{ balance }}, Sorry! Insufficient Funds
          </p>
          <button type="button" class="btn btn-success">Request Overdraft</button>
        </div>
        <input
          v-model="formData.amount"
          type="text"
          id="amount"
          name="amount"
          placeholder="Enter Amount"
          @input="check_balance"
        />
      </div>

      <!-- Remarks -->
      <div class="form-group">
        <textarea
          v-model="formData.remarks"
          id="remarks"
          name="remarks"
          placeholder="Remarks"
        ></textarea>
      </div>

      <!-- Network Selection -->
      <div class="form-group">
        <label for="network" class="form-label">Choose Network</label>
        <div class="radio-group">
          <label class="radio-option">
            <input type="radio" name="network" value="Safaricom" />
            Safaricom
          </label>
          <label class="radio-option">
            <input type="radio" name="network" value="Airtel" />
            Airtel
          </label>
          <label class="radio-option">
            <input type="radio" name="network" value="Telkom" />
            Telkom
          </label>
        </div>
      </div>

      <!-- PIN Input -->
      <div class="form-group">
        <input
          v-model="formData.password"
          type="password"
          id="password"
          name="password"
          placeholder="PIN"
          style="background-color: rgb(0, 19, 31); border: none; border-bottom: 1px solid aqua; width: 25%;"
        />
      </div>

      <!-- Submit Button -->
      <button type="button" class="btn btn-success" @click="showConfirmation">
        Buy Goods
      </button>
    </form>

    <!-- Confirmation Modal -->
    <div class="modal-overlay" v-if="isConfirmationVisible">
      <div class="modal-card-">
        <h2 class="modal-title-">Confirm Details</h2>
        <p class="modal-content-">Store: <span>{{ formData.beneficiary }}</span></p>
        <p class="modal-content-">Amount: <span>{{ formData.amount }}</span></p>
        <p class="modal-content-">Source Account: <span>{{ formData.account }}</span></p>
        <p class="modal-content-">Description: <span>{{ formData.remarks }}</span></p>
        <div v-if="!isProcessing" class="modal-buttons-">
          <button class="modal-btn- confirm" @click="confirmTransfer">Yes</button>
          <button class="modal-btn- cancel" @click="cancelTransfer">Cancel</button>
        </div>
        <div v-if="isProcessing">
          <p class="wait">Processing <i class="fa-regular wait fa-clock fa-spin"></i></p>
        </div>
      </div>
    </div>
  </div>
  <Footer></Footer>
</template>

<script>
import utils from "../../utils/utils";
import Nav_Bar from "../../components/navbar.vue";
import apiEndpoints from '@/api/apiEndpoints';
import Footer from "@/components/others/footer.vue";

export default {
  name: "Buy_goods",
  components: {
    Nav_Bar, Footer
  },
  data() {
    /**
     * Component's reactive data.
     */
    return {
      // Form data to store input values
      formData: {
        amount: "",        // The amount for the transaction
        remarks: "",       // Optional remarks for the transaction
        beneficiary: "",   // The store number to which the payment will be made
        account: "",       // Selected account to debit
        password: "",      // User PIN/password for authorization
      },
      all_accounts: [],       // List of accounts fetched from the backend
      isConfirmationVisible: false, // Flag to toggle the confirmation modal visibility
      isProcessing: false,    // Flag to indicate processing status of the transaction
      balance: "",            // Calculated account balance after the transaction
    };
  },
  mounted() {
    /**
     * Lifecycle hook that runs after the component is mounted.
     * Fetches the user's account data.
     */
    this.fetchData();
  },
  methods: {
    async fetchData() {
      /**
       * Fetches all user accounts from the backend API.
       */
      try {
        const response = await fetch(apiEndpoints.accounts.getTransactiveaccounts, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`, // Authorization token
          },
        });
        const data = await response.json(); // Parses the JSON response
        this.all_accounts.push(...data);   // Updates the accounts list
      } catch (error) {
        console.error("Error fetching data:", error); // Handles any fetch errors
      }
      try {
        const response = await fetch(apiEndpoints.loans.getTransactiveloans, {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });

        const data = await response.json();
        this.all_accounts.push(...data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    showConfirmation() {
      /**
       * Displays the confirmation modal if all required fields are filled.
       */
      if (utils.checkEmptyValues(this.formData)) {
        alert("Please fill in all required fields."); // Alert for missing input fields
        return;
      }
      this.isConfirmationVisible = true; // Show confirmation modal
    },
    confirmTransfer() {
      /**
       * Initiates the buyGoods transaction and sets the processing flag.
       */
      this.buyGoods(); // Performs the transaction
      this.isProcessing = true; // Sets the processing state
    },
    cancelTransfer() {
      /**
       * Cancels the confirmation modal and hides it.
       */
      this.isConfirmationVisible = false; // Hide confirmation modal
    },
    check_balance() {
      const balance = utils.checkBalance(this.formData.account,
      this.formData.amount, this.all_accounts
      )
      this.balance = balance
    },
    async buyGoods() {
      /**
       * Sends a POST request to initiate a "Buy Goods" transaction.
       */
      try {
        // Prepare request body with HMAC signature for security
        const requestBody = utils.generateHmacSignature({
          amount: Number(this.formData.amount),
          account: this.findAndReturnSubsequent(this.formData.account, ":"),
          remarks: this.formData.remarks,
          beneficiary: this.formData.beneficiary,
        });

        // POST request to the backend API
        const response = await fetch(apiEndpoints.transactions.buyGoods, {
          method: "POST",
          headers: {
            "Content-Type": "application/json", // JSON format
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`, // Authorization token
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error("Failed to post data"); // Error handling for unsuccessful response
        }
        // Redirect to the success page after processing
        setTimeout(() => {
          this.$router.push("/success");
        }, 2000);
      } catch (error) {
        console.error("Error posting data:", error); // Logs errors during the transaction
        // Redirect to an error page
        setTimeout(() => {
          this.$router.push("/error");
        }, 2000);
      }
    },
    findAndReturnSubsequent(str, char) {
      /**
       * Helper function to find the substring after a specific character in a string.
       * @param {string} str - The input string.
       * @param {string} char - The character to find in the string.
       * @returns {string} The substring after the character, or an empty string if not found.
       */
      const index = str.indexOf(char); // Get the position of the character
      return index !== -1 && index < str.length - 1
        ? str.substring(index + 1) // Return substring after the character
        : "";
    },
  },
};
</script>

<style scoped>
h1 {
  color: gold;
  margin-left: 5px;
}
form {
  margin-left: 10px;
  margin-top: 80px;
}
label {
  color: white;
}
span {
  color: green;
}
</style>
