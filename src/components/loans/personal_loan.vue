<template>
<div class="container">
    <h1>Personal Loan Application</h1>
    <form action="/submit-loan" method="POST">

        <!-- Financial Information Section -->
        <div class="form-section">
            <h2>Financial Information</h2>
            <label for="employment-status">Employment Status <span class="required">*</span></label>
            <select v-model="formData.employment_status" id="employment-status" name="employment_status" required>
                <option value="">Select Status</option>
                <option value="salaried">Salaried</option>
                <option value="self-employed">Self-Employed</option>
                <option value="unemployed">Unemployed</option>
            </select>

            <label for="monthly-income">Monthly Income (in USD) <span class="required">*</span></label>
            <input v-model="formData.monthly_income" type="number" id="monthly-income" name="monthly_income" required>

            <label for="existing-loans">Do you have existing loans? <span class="required">*</span></label>
            <select id="existing-loans" name="existing_loans" required>
                <option value="">Select</option>
                <option value="yes">Yes</option>
                <option value="no">No</option>
            </select>

        </div>

        <!-- Loan Requirements Section -->
        <div class="form-section">
            <h2>Loan Requirements</h2>
            <label for="loan-amount">Loan Amount Requested (in USD) <span class="required">*</span></label>
            <input v-model="formData.loan_amount" type="number" id="loan-amount" name="loan_amount" required>

            <label for="loan-purpose">Purpose of Loan <span class="required">*</span></label>
            <textarea v-model="formData.purpose" id="loan-purpose" name="loan_purpose" rows="3" required></textarea>

            <label for="repayment-period">Repayment Period (in months) <span class="required">*</span></label>
            <input v-model="formData.repayment_period" type="number" id="repayment-period" name="repayment_period" required>
        </div>

        <button @click.prevent="showConfirmation" type="submit" class="btn-submit">Submit Application</button>
    </form>
</div>
<div class="modal-overlay" v-if="isConfirmationVisible">
    <div class="modal-card">
      <h2 class="modal-title">Confirm Details</h2>
      <p class="modal-content">
        Loan Amount: <span>{{ formData.loan_amount }}</span>
      </p>
      <p class="modal-content">
        Repayment Period: <span>{{ formData.repayment_period }}</span>
      </p>
      <p class="modal-content">
        Purpose: <span>{{ formData.purpose }}</span>
      </p>
      <p class="modal-content">
        Ratw: <span>Fixed at 7.54</span>
      </p>
      <p id="info">Your loan application will be reviewed. <br>
        Succesful loans will be automatically accessible. <br>
        If the bank requires further documentation, please be ready to share
      </p>

      <div v-if="!isProcessing" class="modal-buttons">
        <button class="modal-btn confirm" @click="confirmTransfer">Yes</button>
        <button class="modal-btn cancel" @click="cancelTransfer">Cancel</button>
      </div>
      <div v-if="isProcessing">
        <p class="wait">Processing<i class="fa-regular wait fa-clock fa-spin"></i></p>
      </div>
    </div>
  </div>
</template>
  
    
    
  <script>
  import utils from '../../utils/utils';
  /*import Terms_Conditions from '../../components/account_opening/terms_and_conditions.vue';*/
  const url = 'http://127.0.0.1:8000/post/apply_personal_loan';
  
  export default {
    name: 'Personal_Loan',
    components: {

    },
    data() {
      return {
        formData: {
          monthly_income: '',
          employment_status: '',
          repayment_period: '',
          loan_amount: '',
          purpose: '',
        },
        isTermsChecked: false,
        isConfirmationVisible: false,
        isProcessing: false,
        showTerms: false,
      };
    },
    methods: {
      async applyLoan() {
        try {
  
          const requestBody = utils.generateHmacSignature({
            monthly_income: this.formData.monthly_income,
            employment_status: this.formData.employment_status,
            amount: this.formData.loan_amount,
            purpose: this.formData.purpose,
            payback_period: this.formData.repayment_period,
          });
          console.log(requestBody)
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
            },
            body: JSON.stringify(requestBody)
          });
  
          if (!response.ok) {
            throw new Error('Failed to post data');
          }
  
          this.success = true;
          setTimeout(() => this.$router.push('/success'), 2000);
        } catch (error) {
          console.error('Error posting data:', error);
          setTimeout(() => this.$router.push('/failed'), 500);
        }
      },
  
      toggleTerms() {
        this.showTerms = !this.showTerms;
      },
  
      confirmTransfer() {
        this.applyLoan();
        this.isProcessing = true;
      },
  
      cancelTransfer() {
        this.isConfirmationVisible = false;
      },
  
      showConfirmation() {
        /*if (!this.isTermsChecked) {
          return;
        }*/
        if (utils.checkEmptyValues(this.formData)) {
          alert('Please fill in all required fields.');
          return;
        }
        this.isConfirmationVisible = true;
      },
    },
  };
  </script>
  
  
  <style scoped>
        .container {
            max-width: 800px;
            margin: 20px auto;
            background: rgb(0, 19, 31);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            color: gold;
        }

        form {
            display: flex;
            flex-direction: column;
        }

        label {
            margin-top: 15px;
            font-weight: bold;
            color: white;
        }

        input, select, textarea {
            margin-top: 5px;
            padding: 10px;
            font-size: 16px;
            border: 1px solid aqua;
            border-radius: 4px;
            width: 100%;
            box-sizing: border-box;
        }

        input:focus, select:focus, textarea:focus {
            border-color: gold;
            outline: none;
        }

        .form-group {
            margin-top: 10px;
        }

        .form-section {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid aqua;
            border-radius: 8px;
            background-color: rgb(0, 19, 31);
        }

        .form-section h2 {
            margin-top: 0;
            color: gold;
        }

        .btn-submit {
            margin-top: 20px;
            padding: 15px;
            font-size: 16px;
            color: #ffffff;
            background-color: #007BFF;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        .btn-submit:hover {
            background-color: #0056b3;
        }

        .required {
            color: red;
        }
        select, #repayment-period, #loan-amount, #monthly-income {
          background-color: rgb(0, 19, 31);
          color: white;
        }
        span {
          color: green;
        }
        #info {
          color: white;
          font-family: Arial, Helvetica, sans-serif;
          font-style: italic;
        }
  </style>
  