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
      <button type="button" class="btn btn-success" @click="applyCard">Apply Now</button>
    </form>
  </div>
</template>
<script>
import Nav_Bar from '../../components/navbar.vue'
import utils from '../../utils/utils'
const url2 = "http://127.0.0.1:8000/post/get_user_personal_accounts";
    export default {
        name: "Debit_App",
        components: {
          Nav_Bar
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
        const response = await fetch(url2, {
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
      const response = await fetch('http://127.0.0.1:8000/post/debit_card_application', {
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
      }
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
      background-color: #007bff;
      color: white;
      font-weight: bold;
      cursor: pointer;
      border: none;
    }
    button:hover {
      background-color: #0056b3;
    }
    input, select{
      background-color: rgb(0, 19, 31);
      color: white;
    }
</style>