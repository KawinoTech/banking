<template>
  <Nav_Bar></Nav_Bar>
  <form action="#">
    <h1>Send Money</h1>
    <label for="account" class="form-label">Choose Account</label>
    <select 
      id="account" 
      name="account" 
      v-model="formData.account" 
      class="form-select"
    >
      <option 
        v-for="account in all_accounts" 
        :key="account"
      >
        {{account.account_type}} {{account.currency}}:{{account.account_no}}
      </option>
    </select>

    <div class="form-group">
      <p 
        v-if="balance > 0 && formData.amount !== ''" 
        class="within_limit"
      >
        Balance: {{balance}}
      </p>
      <div 
        class="overdraft" 
        v-else-if="balance < 0 && formData.amount !== ''"
      >
        <p class="exceed_limit">
          Balance: {{balance}}, Sorry! Insufficient Funds
        </p>
        <button 
          type="button" 
          class="btn btn-success"
        >
          Request Overdraft
        </button>
      </div>
      <input 
        type="text" 
        id="amount" 
        name="amount" 
        v-model="formData.amount" 
        placeholder="Enter Amount" 
        @input="check_balance"
      >
    </div>

    <div class="form-group">
      <input 
        type="text" 
        id="beneficiary" 
        name="beneficiary" 
        v-model="formData.beneficiary" 
        placeholder="Enter Beneficiary"
      >
    </div>

    <div class="form-group">
      <textarea 
        id="remarks" 
        name="remarks" 
        v-model="formData.remarks" 
        placeholder="Remarks"
      >
      </textarea>
    </div>

    <div class="form-group">
      <input 
        type="password" 
        id="password" 
        v-model="password" 
        name="password" 
        placeholder="PIN" 
      >
    </div>

    <button 
      type="button" 
      class="btn btn-success" 
      @click="showConfirmation"
    >
      Transfer Funds
    </button>
  </form>

  <div 
    class="modal-overlay" 
    v-if="isConfirmationVisible"
  >
    <div class="modal-card-">
      <h2 class="modal-title-">Confirm Details</h2>
      <p class="modal-content-">
        Beneficiary: <span>{{ formData.beneficiary }}</span>
      </p>
      <p class="modal-content-">
        Amount: <span>{{ formData.amount }}</span>
      </p>
      <p class="modal-content-">
        Source Account: <span>{{ formData.account }}</span>
      </p>
      <p class="modal-content-">
        Description: <span>{{ formData.remarks }}</span>
      </p>

      <div 
        v-if="!isProcessing" 
        class="modal-buttons-"
      >
        <button 
          class="modal-btn- confirm" 
          @click="confirmTransfer"
        >
          Yes
        </button>
        <button 
          class="modal-btn- cancel" 
          @click="cancelTransfer"
        >
          Cancel
        </button>
      </div>

      <div 
        v-if="isProcessing"
      >
        <p class="wait">
          Processing <i class="fa-regular wait fa-clock fa-spin"></i>
        </p>
      </div>
    </div>
  </div>
  <Footer></Footer>
</template>

<script>
/**
 * Script for the "Transfer Funds" component.
 * This component handles fund transfers, including form validation, data submission,
 * confirmation modals, and user account fetching.
 */

import apiEndpoints from '@/api/apiEndpoints';
import Nav_Bar from '../../components/navbar.vue';
import utils from '../../utils/utils';
import Footer from '@/components/others/footer.vue';

export default {
  name: "Transfer_Funds",
  components: {
    Nav_Bar, Footer
  },
  data() {
    return {
      formData: {
        account: '',
        amount: '',
        remarks: '',
        beneficiary: '',
      },
      password: '', // Stores the user's entered PIN or password
      isConfirmationVisible: false, // Controls the visibility of the confirmation modal
      isProcessing: false, // Indicates if a transfer is being processed
      all_accounts: [], // List of user accounts fetched from the server
      balance: ''
    };
  },
  mounted() {
    // Fetch data when the component is mounted
    this.fetchData();
  },
  methods: {
    /**
     * Finds and returns the part of a string after the first occurrence of a specific character.
     * @param {string} str - The input string.
     * @param {string} char - The character to search for.
     * @returns {string} The substring following the character or an empty string if not found.
     */
    findAndReturnSubsequent(str, char) {
      const index = str.indexOf(char);
      return index !== -1 && index < str.length - 1
        ? str.substring(index + 1)
        : "";
    },

    /**
     * Checks the balance of the selected account after the amount is entered.
     * Updates the `balance` value for the selected account.
     */
    check_balance() {
      const balance = utils.checkBalance(this.formData.account,
      this.formData.amount, this.all_accounts
      )
      this.balance = balance
    },

    /**
     * Displays the confirmation modal if all form fields are valid.
     */
    showConfirmation() {
      if (utils.checkEmptyValues(this.formData)) {
        alert('Please fill in all required fields.');
        return;
      }
      this.isConfirmationVisible = true;
    },

    /**
     * Initiates the fund transfer process and shows the processing state.
     */
    confirmTransfer() {
      this.transferFunds();
      this.isProcessing = true;
    },

    /**
     * Closes the confirmation modal.
     */
    cancelTransfer() {
      this.isConfirmationVisible = false;
    },

    /**
     * Handles the actual fund transfer by sending data to the backend API.
     * Includes error handling for network or API failures.
     */
    async transferFunds() {
      try {
        const requestBody = utils.generateHmacSignature({
          amount: Number(this.formData.amount),
          account: this.findAndReturnSubsequent(this.formData.account, ':'),
          remarks: this.formData.remarks,
          beneficiary: this.formData.beneficiary,
        });

        const response = await fetch(apiEndpoints.transactions.c2bTransfer, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error('Failed to post data');
        }

        setTimeout(() => {
          this.isConfirmationVisible = false;
          this.isProcessing = false;
          this.$router.push('/success');
        }, 3000);
      } catch (error) {
        console.error('Error posting data:', error);
        setTimeout(() => {
          this.isConfirmationVisible = false;
          this.isProcessing = false;
          this.$router.push('/failed');
        }, 1000);
      }
    },

    /**
     * Fetches the user's transactive accounts from the backend API.
     * Updates `all_accounts` with the fetched data.
     */
    async fetchData() {
      try {
        const response = await fetch(apiEndpoints.accounts.getTransactiveaccounts, {
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
  },
};
</script>

<style scoped>
h1 {
  color: gold; margin-left: 5px;
}
label {
  color: antiquewhite;
  margin-left: 20px;
}
form {
  margin-left: 10px;
  margin-top: 80px
}

span {
  color: green;
}

select {
  background-color: rgb(0, 19, 31);
  color: white; 
  width: 50%;
}
#password {
  width: 25%;
}
</style>
