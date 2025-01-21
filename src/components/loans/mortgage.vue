<template>
<div class="container">
    <h1>Mortgage Application</h1>
    <form action="/submit-mortgage-application" method="POST">
        <!-- Personal Details Section -->
        <div class="form-section">
            <h2>Personal Details</h2>
            <label for="full-name">Full Name <span class="required">*</span></label>
            <input v-model="formData.account_name" type="text" id="full-name" name="full_name" required>

            <label for="current-address">Current Address <span class="required">*</span></label>
            <textarea id="current-address" name="current_address" rows="3" required></textarea>

            <label for="employment-status">Employment Status <span class="required">*</span></label>
            <select v-model="formData.employment_status" id="employment-status" name="employment_status" required>
                <option value="">Select</option>
                <option value="salaried">Salaried</option>
                <option value="self-employed">Self-Employed</option>
                <option value="unemployed">Unemployed</option>
            </select>
        </div>

        <!-- Property Details Section -->
        <div class="form-section">
            <h2>Property Details</h2>
            <label for="property-address">Property Address <span class="required">*</span></label>
            <textarea v-model="formData.property_address" id="property-address" name="property_address" rows="3" required></textarea>

            <label for="property-value">Estimated Property Value (in USD) <span class="required">*</span></label>
            <input v-model="formData.property_value" type="number" id="property-value" name="property_value" required>

            <label for="down-payment">Down Payment (in USD) <span class="required">*</span></label>
            <input v-model="formData.down_payment" type="number" id="down-payment" name="down_payment" required>

            <label for="property-type">Property Type <span class="required">*</span></label>
            <select v-model="formData.property_type" id="property-type" name="property_type" required>
                <option value="">Select</option>
                <option value="residential">Residential</option>
                <option value="commercial">Commercial</option>
                <option value="land">Land</option>
            </select>
        </div>

        <!-- Financial Details Section -->
        <div class="form-section">
            <h2>Financial Information</h2>
            <label for="annual-income">Annual Income (in USD) <span class="required">*</span></label>
            <input v-model="formData.annual_income" type="number" id="annual-income" name="annual_income" required>


            <label for="existing-mortgages">Do you have existing mortgages? <span class="required">*</span></label>
            <select id="existing-mortgages" name="existing_mortgages" required>
                <option value="">Select</option>
                <option value="yes">Yes</option>
                <option value="no">No</option>
            </select>

            <div>
                <h3 style="display: inline;">Tax Compliance</h3>
                <input class="docs" type="file" @change="handleFileUpload1" />
            </div>
            <div>
                <h3 style="display: inline;">CRB Listing</h3>
                <input class="docs" type="file" @change="handleFileUpload2" />
            </div>
            <div>
                <h3 style="display: inline;">Recent Pay Slips</h3>
                <input class="docs" type="file" @change="handleFileUpload3" />
            </div>
            <div>
                <h3 style="display: inline;">Proof of down payment</h3>
                <input class="docs" type="file" @change="handleFileUpload4" />
            </div>
            <div>
                <h3 style="display: inline;">Purchase agreement</h3>
                <input class="docs" type="file" @change="handleFileUpload5" />
            </div>
        </div>

        <!-- Loan Requirements Section -->
        <div class="form-section">
            <h2>Loan Requirements</h2>
            <label for="loan-amount">Requested Loan Amount (in USD) <span class="required">*</span></label>
            <input v-model="formData.amount" type="number" id="loan-amount" name="loan_amount" required>

            <label for="loan-term">Loan Term (in years) <span class="required">*</span></label>
            <input v-model="formData.payback_period" type="number" id="loan-term" name="loan_term" required>

            <label for="interest-rate">Preferred Interest Rate (%)</label>
            <input v-model="formData.rate" type="number" id="interest-rate" name="interest_rate">
        </div>

        <button @click.prevent="applyLoan" type="submit" class="btn-submit">Submit Application</button>
    </form>
</div>
    </template>
  
    
    
  <script>
  import utils from '../../utils/utils';
  /*import Terms_Conditions from '../../components/account_opening/terms_and_conditions.vue';*/
  
  const url = 'http://127.0.0.1:8000/post/apply_mortgage';
  
  export default {
    name: 'Mortgage_Facility',
    components: {
    },
    data() {
      return {
        formData: {
          account_name: '',
          property_address: '',
          property_value: '',
          down_payment: '',
          amount: '',
          property_type: '',
          payback_period: '',
          employment_status: '',
          annual_income: '',
          rate: '',
        },
        isConfirmationVisible: false,
        isProcessing: false,
        tax_cert: null,
        crb: null,
        pay_slip: null,
        down_payment: null,
        purchase_agreement: null,
        showTerms: false,
        isTermsChecked: false,
      };
    },
    methods: {
      async applyLoan() {
        try {
          const formData = new FormData();
          formData.append('tax_cert', this.tax_cert);
          formData.append('crb', this.crb);
          formData.append('pay_slip', this.pay_slip);
          formData.append('down_payment', this.down_payment);
          formData.append('purchase_agreement', this.purchase_agreement);
  
          const requestBody = utils.generateHmacSignature({
            account_name: this.formData.account_name,
            employment_status: this.formData.employment_status,
            annual_income: this.formData.annual_income,
            payback_period: this.formData.payback_period,
            property_address: this.formData.property_address,
            property_value: this.formData.property_value,
            down_payment: this.formData.down_payment,
            amount: this.formData.amount,
            property_type: this.formData.property_type,
            rate: this.formData.rate,
          });
          formData.append('signature', requestBody['signature']);
          formData.append('payload', JSON.stringify(requestBody['payload']));
          for (let [key, value] of formData.entries()) {
            console.log(key, value)
          }
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
            },
            body: formData,
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
      checkAccNameInput() {
        const namePattern = /^[A-Z][a-z]* [A-Z][a-z]* [A-Z][a-z]*$/;
        this.isValidaccount_name = namePattern.test(this.formData.account_name);
      },
      handleFileUpload1(event) {
        this.tax_cert = event.target.files[0];
      },
      handleFileUpload2(event) {
        this.crb = event.target.files[0];
      },
      handleFileUpload3(event) {
        this.pay_slip = event.target.files[0];
      },
      handleFileUpload4(event) {
        this.down_payment = event.target.files[0];
      },
      handleFileUpload5(event) {
        this.purchase_agreement = event.target.files[0];
      },
      showConfirmation() {
        if (!this.isTermsChecked) return;
        if (utils.checkEmptyValues(this.formData)) {
          alert('Please fill in all required fields.');
          return;
        }
        this.isConfirmationVisible = true;
      },
      toggleTerms() {
        this.showTerms = !this.showTerms;
      },
      confirmTransfer() {
        this.createAccount();
        this.isProcessing = true;
      },
      cancelTransfer() {
        this.isConfirmationVisible = false;
      },
      checkTelephoneInput() {
          const namePattern = /^\+\d{1,3}\s\d{9}$/;
          if (namePattern.test(this.formData.telephone)) {
            this.isValidtelephone = true;
          }
          else {
            this.isValidtelephone = false;
          }
        },
        checkEmailInput() {
          const namePattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
          if (namePattern.test(this.formData.email)) {
            this.isValidemail = true;
          }
          else {
            this.isValidemail = false;
          }
        },
    },
  };
  </script>
    
<style scoped>
.container {
    max-width: 900px;
    margin: 20px auto;
    background: rgb(0, 19, 31);;
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
    background-color: rgb(0, 19, 31);;
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
select,
#repayment-period,
#loan-amount,
#annual-income,
#property-value,
#down-payment,
#loan-term,
#interest-rate, #phone {
  background-color: rgb(0, 19, 31);
  color: white;
}
.docs {
          margin: 20px 0px 20px 0px;
          color: aqua;
        }
        #info {
          color: white;
          font-family: Arial, Helvetica, sans-serif;
          font-style: italic;
        }
        h3 {
          color: white;
          font-size: medium;
        }
</style>
    