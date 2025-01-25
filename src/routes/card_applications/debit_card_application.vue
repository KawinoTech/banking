<template>
  <Nav_Bar></Nav_Bar>
    <div class="form-container">
    <h1>Debit Card Application</h1>
    <form action="/submit-debit-card-application" method="POST">
      <!-- Personal Information -->
      <label for="full_name">Full Name</label>
      <input v-model="formData.full_name" type="text" id="full_name" name="full_name" placeholder="Enter your full name" required>

      <label for="email">Email Address</label>
      <input v-model="formData.email" type="email" id="email" name="email" placeholder="Enter your email address" required>

      <label for="phone">Phone Number</label>
      <input v-model="formData.phone" type="tel" id="phone" name="phone" placeholder="Enter your phone number" required>

      <!-- Account Details -->
      <label for="account_number">Attach to Account</label>
      <select v-model="formData.account_number" id="account_number" name="account_number" required>
        <option v-for="account in all_accounts" :key="account">
            {{account.account_type}} {{account.currency}}:{{account.account_no}}
          </option>
      </select>

      <!-- Card Preferences -->
      <label for="card_classification">Card Type</label>
      <select v-model="formData.card_classification" id="card_classification" name="card_classification" required>
        <option value="Classic Debit Card">Classic Debit Card</option>
        <option value="Platinum Debit Card">Platinum Debit Card</option>
        <option value="Premium Debit Card">Premium Debit Card</option>
      </select>

      <label for="delivery_option">Delivery Option</label>
      <select v-model="formData.delivery_option" id="delivery_option" name="delivery_option" required>
        <option value="branch">Pick up at branch</option>
        <option value="mail">Mail to address</option>
      </select>

      <!-- Terms and Clonditions -->
      <label>
        <input type="checkbox" name="terms" required>
        I agree to the terms and conditions.
      </label>

      <!-- Submit Button -->
      <button type="button" class="btn btn-success" @click="showConfirmation">Apply Now</button>
    </form>
  </div>
  <div class="modal-overlay" v-if="isConfirmationVisible">
      <div class="modal-card-">
        <h2 class="modal-title-">Confirm Details</h2>
        <p class="modal-content-">
          Card Name: <span>{{ formData.full_name }}</span>
        </p>
        <p class="modal-content-">
          Account: <span>{{ formData.account_number }}</span>
        </p>
        <p class="modal-content-">
          Delivery: <span>{{ formData.delivery_option }}</span>
        </p>
        <p class="modal-content-">
          Classification: <span>{{ formData.card_classification }}</span>
        </p>
        <p id="details" class="modal-content-">
          Dear Customer, our team will follow up immediately and <br>
          Notify you of your debit card processing This will happen<br>in the next 24hrs
          Thank you for choosing Vue JS Bank <br>
        </p>
        <div v-if="!isProcessing" class="modal-buttons-">
          <button class="modal-btn- confirm" @click="confirm">Yes</button>
          <button class="modal-btn- cancel" @click="cancel">Cancel</button>
        </div>
        <div v-if="isProcessing">
          <p class="wait">
            Processing<i class="fa-regular wait fa-clock fa-spin"></i>
          </p>
        </div>
      </div>
    </div>
    <Footer></Footer>
</template>
<script>
import Nav_Bar from '../../components/navbar.vue'
import utils from '../../utils/utils'
import apiEndpoints from '@/api/apiEndpoints';
import Footer from '@/components/others/footer.vue';
    export default {
        name: "Debit_App",
        components: {
          Nav_Bar, Footer
        },
        data() {
    return {
      formData: {
        full_name: "",
        email: "",
        phone: "",
        account_number: "",
        delivery_option: "",
        card_classification: "",
      },
      all_accounts: [],
      isConfirmationVisible: false,
      isProcessing: false,
    };
  },
  mounted() {
        this.fetchData();
      },
  methods: {
    async fetchData() {
      try {
        const response = await fetch(apiEndpoints.accounts.getTransactiveaccounts, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        const data = await response.json();
        this.all_accounts.push(...data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    findAndReturnSubsequent(str, char) {
      const index = str.indexOf(char);
      return index !== -1 && index < str.length - 1
        ? str.substring(index + 1)
        : "";
    },
    async applyCard() {
      try{
          if (utils.checkEmptyValues(this.formData)){
            throw new Error('Empty Fields');
      }
      const requestBody = utils.generateHmacSignature( {"delivery_option": this.formData.delivery_option,
                          "account_attached_no": this.findAndReturnSubsequent(this.formData.account_number, ':'),
                          "phone": this.formData.phone,
                          "email_address": this.formData.email,
                          "full_name": this.formData.full_name,
                        "card_classification": this.formData.card_classification})
      const response = await fetch(apiEndpoints.cardService.applyDebitCard, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                        },
                        body: JSON.stringify(requestBody)
                        }
                       );
      if (!response.ok) {
      throw new Error('Failed to post data');
      }
      setTimeout(() => {
            this.isConfirmationVisible = false;
            this.isProcessing = false;
            this.$router.push('/success');
          }, 3000);
         }
         catch (error) {
            console.error('Error posting data:', error);
            setTimeout(() => {
              this.isConfirmationVisible = false;
              this.isProcessing = false;
              this.$router.push('/failed');
            }, 1000);
            // Handle error if necessary
         }
      },
      confirm() {
      /**
       * Initiates the bill payment process and sets processing status.
       */
      this.applyCard();
      this.isProcessing = true;
    },

    cancel() {
      /**
       * Cancels and hides the confirmation modal.
       */
      this.isConfirmationVisible = false;
    },

    showConfirmation() {
      /**
       * Validates required fields and shows the confirmation modal.
       */
      if (utils.checkEmptyValues(this.formData)) {
        alert("Please fill in all required fields.");
        return;
      }
      this.isConfirmationVisible = true;
    },
  }
}
</script>
<style scoped>
    .form-container {
      background-color: rgb(0, 19, 31);
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      width: 50%;
      padding: 20px;
      margin-top: 80px;
    }
    h1 {
  color: gold; margin-left: 5px;
}
    label {
      font-weight: bold;
      margin-bottom: 5px;
      display: block;
      color: white;
    }
    input, select, button {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border: 1px solid aqua;
      border-radius: 5px;
    }
    button {
      background-color: rgba(0, 128, 0, 0.719);
      color: white;
      font-weight: bold;
      cursor: pointer;
      border: none;
      width: 20%;
    }
    button:hover {
      background-color: green
    }
    input, select{
      background-color: rgb(0, 19, 31);
      color: white;
    }
    span {
      color: green;
    }
    #details {
      color: white;
    }
</style>