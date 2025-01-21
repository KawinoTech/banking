<template>
  <div class="container">
    <h1>Business Loan Application</h1>
    <form action="/submit-business-loan" method="POST">
        <!-- Business Details Section -->
        <div class="form-section">
            <h2>Business Details</h2>
            <label for="business-name">Business Name <span class="required">*</span></label>
            <input v-model="formData.account_name" type="text" id="business-name" name="business_name" required>

            <label for="registration-number">Business Registration Number <span class="required">*</span></label>
            <input v-model="formData.id_no" type="text" id="registration-number" name="registration_number" required>

            <label for="business-type">Type of Business <span class="required">*</span></label>
            <select v-model="formData.business_type" id="business-type" name="business_type" required>
                <option value="">Select Type</option>
                <option value="sole-proprietorship">Sole Proprietorship</option>
                <option value="partnership">Partnership</option>
                <option value="corporation">Corporation</option>
                <option value="llc">LLC</option>
            </select>

            <label for="establishment-date">Date of Establishment <span class="required">*</span></label>
            <input v-model="formData.dob" type="date" id="establishment-date" name="establishment_date" required>

            <label for="business-address">Business Address <span class="required">*</span></label>
            <textarea v-model="formData.address" id="business-address" name="business_address" rows="3" required></textarea>

            <label for="industry">Industry/Sector <span class="required">*</span></label>
            <input v-model="formData.industry" type="text" id="industry" name="industry" required>
        </div>

        <!-- Financial Information Section -->
        <div class="form-section">
            <h2>Financial Information</h2>
            <label for="annual-revenue">Annual Revenue (in USD) <span class="required">*</span></label>
            <input v-model="formData.annual_income" type="number" id="annual-revenue" name="annual_revenue" required>

            <label for="profit-margin">Profit Margin (%) <span class="required">*</span></label>
            <input v-model="formData.pmargin" type="number" id="profit-margin" name="profit_margin" required>

            <label for="existing-loans">Existing Loans <span class="required">*</span></label>
            <select id="existing-loans" name="existing_loans" required>
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
                <h3 style="display: inline;">CR12/ Registration Document</h3>
                <input class="docs" type="file" @change="handleFileUpload3" />
            </div>
            <div>
                <h3 style="display: inline;">Bank Statements/Utility Bills</h3>
                <input class="docs" type="file" @change="handleFileUpload4" />
            </div>
        </div>

        <!-- Loan Requirements Section -->
        <div class="form-section">
            <h2>Loan Requirements</h2>
            <label for="loan-amount">Loan Amount Requested (in USD) <span class="required">*</span></label>
            <input v-model="formData.amount" type="number" id="loan-amount" name="loan_amount" required>

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
        Loan Amount: <span>{{ formData.amount }}</span>
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
  import utils from "../../utils/utils";
  /*import Account_Signatories from "./signatories.vue"; will work on this feature later*/
  /*import Terms_Conditions from "../../components/account_opening/terms_and_conditions.vue";*/
  
  const url = "http://127.0.0.1:8000/post/apply_business_loan";
  
  export default {
    name: "Business_Loan",
    data() {
      return {
        formData: {
          account_name: "",
          purpose: "",
          address: "",
          id_no: "",
          business_type: "",
          amount: "",
          dob: "",
          pmargin: "",
          annual_income: "",
          repayment_period: "",
        },
        isValidaccount_name: false,
        isValidtelephone: false,
        isValidemail: false,
        isTermsChecked: false,
        isConfirmationVisible: false,
        isProcessing: false,
        showTerms: false,
        tax_cert: null,
        crb: null,
        reg_cert: null,
        operational_docs: null,
      };
    },
    /*components: { Terms_Conditions },*/
    methods: {
      async applyLoan() {
        try {
          const formData = new FormData();
          formData.append('tax_cert', this.tax_cert);
          formData.append('reg_cert', this.reg_cert);
          formData.append('crb', this.crb);
          formData.append('operational_docs', this.operational_docs);
  
          const requestBody = utils.generateHmacSignature({
            id_no: this.formData.id_no,
            purpose: this.formData.purpose,
            payback_period: this.formData.repayment_period,
            account_name: this.formData.account_name,
            address: this.formData.address,
            pmargin: this.formData.pmargin,
            business_type: this.formData.email,
            dob: this.formData.dob,
            annual_income: this.formData.annual_income,
            amount: this.formData.amount
          });
  
          formData.append('signature', requestBody['signature']);
          formData.append('payload', JSON.stringify(requestBody['payload']));
  
          const response = await fetch(url, {
            method: "POST",
            headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
            body: formData,
          });
          if (!response.ok) throw new Error("Failed to post data");
  
          this.$router.push("/success");
        } catch (error) {
          console.error("Error posting data:", error);
          this.$router.push("/failed");
        }
      },
      checkAccNameInput() {
          const namePattern = /^[A-Z][a-z]* [A-Z][a-z]* [A-Z][a-z]*$/;
          if (namePattern.test(this.formData.account_name)) {
            this.isValidaccount_name = true;
          }
          else {
            this.isValidaccount_name = false;
          }
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
        handleFileUpload1(event) {
          this.tax_cert = event.target.files[0]; // Access the selected file
        },
        handleFileUpload2(event) {
          this.crb = event.target.files[0]; // Access the selected file
        },
        handleFileUpload3(event) {
          this.reg_cert = event.target.files[0]; // Access the selected file
        },
        handleFileUpload4(event) {
          this.operational_docs = event.target.files[0]; // Access the selected file
        },
        toggleTerms() {
          this.showTerms = !this.showTerms;
        },
        showConfirmation() {
        if (utils.checkEmptyValues(this.formData)) {
          alert("Please fill in all required fields.");
          return;
        }
        this.isConfirmationVisible = true;
      },
      confirmTransfer() {
        this.applyLoan();
        this.isProcessing = true;
      },
      cancelTransfer() {
        this.isConfirmationVisible = false;
      }
      /*
      handleUpdate(formDataSign) {
        const array = [];
    for (const [key, value] of formDataSign.entries()) {
      array.push([key, value]);
    }
  
    this.signatories = array;
  }* Will work on this feature later*/
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
            border-color: #007BFF;
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
        select, #repayment-period, #loan-amount, #profit-margin, #annual-revenue, #establishment-date {
          background-color: rgb(0, 19, 31);
          color: white;
        }
        h3 {
          color: white;
          font-size: medium;
        }
        .docs {
          margin: 20px 0px 20px 0px;
          color: aqua;
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
    