<template>
    <Nav_Bar></Nav_Bar>
      <div class="form-container">
    <h1>Credit Card Application</h1>
    <form action="/submit-credit-card-application" method="POST">
      <!-- Personal Information -->
      <label for="full-name">Full Name</label>
      <input v-model="formData.full_name" type="text" id="full_name" name="full_name" placeholder="Enter your full name" required>

      <label for="email">Email Address</label>
      <input v-model="formData.email" type="email" id="email" name="email" placeholder="Enter your email address" required>

      <label for="phone">Phone Number</label>
      <input v-model="formData.phone" type="tel" id="phone" name="phone" placeholder="Enter your phone number" required>

      <!-- Employment Details -->
      <label for="employment_status">Employment Status</label>
      <select v-model="formData.employment_status" id="employment_status" name="employment_status" required>
        <option value="employed">Employed</option>
        <option value="self-employed">Self-Employed</option>
        <option value="student">Student</option>
        <option value="unemployed">Unemployed</option>
        <option value="business">Business</option>
      </select>

      <label for="annual_income">Annual Income (USD)</label>
      <input v-model="formData.annual_income" type="number" id="annual_income" name="annual_income" placeholder="Enter your annual income" required>

      <!-- Card Preferences -->
      <label for="card_classification">Preferred Card Type</label>
      <select v-model="formData.card_classification" id="card_classification" name="card_classification" required>
        <option value="Standard Credit Card">Standard Credit Card</option>
        <option value="Gold Credit Card">Gold Credit Card</option>
        <option value="Platinum Credit Card">Platinum Credit Card</option>
        <option value="Business Credit Card">Business Credit Card</option>
      </select>

      <label for="delivery_option">Delivery Option</label>
      <select v-model="formData.delivery_option" id="delivery_option" name="delivery_option" required>
        <option value="branch">Pick up at branch</option>
        <option value="mail">Mail to address</option>
      </select>

      <!-- Terms and Conditions -->
      <label class="terms">
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
    export default {
        name: "Credit_App",
        components: {
          Nav_Bar
        },
        data() {
    return {
      formData: {
        full_name: "",
        email: "",
        phone: "",
        delivery_option: "",
        card_classification: "",
        annual_income: "",
        employment_status: ""
      },
      all_accounts: [],
      isConfirmationVisible: false,
      isProcessing: false,
    };
  },
  methods: {
    async applyCard() {
      try{
          if (utils.checkEmptyValues(this.formData)){
            throw new Error('Empty Fields');
      }
      const requestBody = utils.generateHmacSignature( {"delivery_option": this.formData.delivery_option,
                          "annual_income": this.formData.annual_income,
                          "employment_status": this.formData.employment_status,
                          "phone": this.formData.phone,
                          "email_address": this.formData.email,
                          "full_name": this.formData.full_name,
                        "card_classification": this.formData.card_classification})
      const response = await fetch('http://127.0.0.1:8000/post/credit_card_application', {
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
              this.$router.push('/error');
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
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
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
      border: none;
      font-weight: bold;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #0056b3;
    }

    .terms {
      font-size: 0.9em;
      color: #555555;
      display: flex;
      align-items: center;
    }

    .terms input {
      margin-right: 10px;
    }
    input, select{
      background-color: rgb(0, 19, 31);
      color: white;
    }
</style>