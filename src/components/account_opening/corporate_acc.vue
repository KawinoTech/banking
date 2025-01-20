<template>
  <h1>
    Open Corporate Account
    <i class="fa-solid fa-circle-question">
      <div class="details">
        <router-link to="/instructions_on_opening_transactional_account">
          <p class="info">Click to find details on account opening</p>
        </router-link>
      </div>
    </i>
  </h1>

  <form action="#" class="account-form">
    <!-- Personal Information -->
    <fieldset>
      <legend>Personal Information</legend>
      <div class="form-group">
        <label for="account_name">Account Name</label>
        <div
          v-if="!isValidaccount_name && formData.account_name"
          class="error-message"
        >
          Account Name MUST contain at least 3 unique names
        </div>
        <input
          v-model="formData.account_name"
          type="text"
          id="account_name"
          name="account_name"
          placeholder="Account Name"
          @input="checkAccNameInput"
        />
      </div>
      <div class="form-group">
          <label for="dob">Date of Incorporation</label>
          <input v-model="formData.dob" type="date" id="dob" name="dob" required />
      </div>

      <div class="form-group">
        <label for="address">Business Nationality</label>
        <input v-model="formData.nationality" type="text" id="nationality" name="nationality" placeholder="Business Nationality"/>
      </div>
  
      <div class="form-group">
        <label for="address">Premise Address</label>
        <input v-model="formData.address" type="text" id="address" name="address" placeholder="Premise Address"/>
      </div>
  
      <div class="form-group">
        <label for="telephone">Telephone</label>
        <div v-if="!isValidtelephone && formData.telephone" class="error-message">
            Incorrect format
        </div>
        <input @input="checkTelephoneInput" v-model="formData.telephone" type="text" id="telephone" name="telephone" placeholder="Telephone" />
      </div>

      <div class="form-group">
        <label for="email">Email Address</label>
        <div v-if="!isValidemail && formData.email" class="error-message">
            Incorrect format
        </div>
        <input @input="checkEmailInput" v-model="formData.email" type="email" id="email" name="email" placeholder="example@domain.com" required />
      </div>
      <!-- Other form fields... -->
    </fieldset>

    <!-- Identification Details -->
    <fieldset>
      <legend>Identification</legend>
      <div class="form-group">
          <label for="id_no">Company Registration Number</label>
          <input v-model="formData.id_no" type="text" id="id_no" name="id_no" placeholder="Company Registration Number" />
        </div>
  
        <div class="form-group">
          <label for="kra_pin">KRA PIN</label>
          <input v-model="formData.kra_pin" type="text" id="kra_pin" name="kra_pin" placeholder="KRA PIN" />
        </div>
    </fieldset>

    <!-- Financial Details -->
    <fieldset>
      <legend>Financial Details</legend>
      <!-- Additional fields go here -->
      <div class="form-group">
          <label for="source_of_funds">Source of Funds</label>
          <input v-model="formData.source_of_funds" type="text" id="usage" name="usage" placeholder="E.g., Farming, Sales" />
        </div>
  
        <div class="form-group">
          <label for="annual_income">Annual Turnover (KES)</label>
          <input v-model="formData.annual_income" type="number" id="annual_income" name="annual_income" placeholder="Enter Annual Income" required />
        </div>
  
        <div class="form-group">
          <label for="usage">Purpose of Account</label>
          <input v-model="formData.intended_usage" type="text" id="usage" name="usage" placeholder="E.g., Online shopping, travel" />
        </div>
    </fieldset>

    <!-- Account Details -->
    <fieldset>
      <legend>Account Details</legend>
      <div class="form-group">
          <label for="account_type">Account Type</label>
          <select v-model="formData.account_type" id="account_type" name="account_type" required>
            <option value="" disabled selected>Select Account Type</option>
            <option>Vue Vantage</option>
            <option>SME Banking</option>
            <option>Vue Corporate</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="currency">Currency</label>
          <select v-model="formData.currency" id="currency" name="currency" required>
            <option value="" disabled selected>Select Currency</option>
            <option>KES</option>
          </select>
        </div>
    </fieldset>

    <!-- Signatories 
    <fieldset>
       <Account_Signatories @updateFormData="handleUpdate"></Account_Signatories>
    </fieldset> Will work on this feature later-->

        <!-- Documentation -->
        <fieldset>
      <legend>Documentation</legend>
      
      <div>
        <h3 style="display: inline;">Tax Compliance</h3>
        <input class="docs" type="file" @change="handleFileUpload1" />
      </div>

      <div>
        <h3 style="display: inline;">Business Registration Certificate</h3>
        <input class="docs" type="file" @change="handleFileUpload2" />
      </div>

      <div>
        <h3 style="display: inline;">Passport Photo</h3>
        <input class="docs" type="file" @change="handleFileUpload3" />
      </div>
    </fieldset>

    <!-- Terms and Conditions -->
    <div class="form-group">
      <label class="terms">
        <input
          v-model="isTermsChecked"
          type="checkbox"
          name="terms"
          required
          @change="toggleTerms"
        />
        I agree to the terms and conditions.
      </label>
      <p style="color: green;">Terms and Conditions {{ isTermsChecked ? 'checked' : 'unchecked' }}</p>
    </div>

    <button
      type="button"
      class="btn btn-success"
      @click.prevent="showConfirmation"
    >
      Open Account
    </button>
  </form>
  <div v-if="showTerms" class="overlay">
    <div class="terms-modal">
      <Terms_Conditions />
    <button class="close-btn" @click="toggleTerms">Close</button>
    </div>
  </div>
  <div v-if="isConfirmationVisible" class="modal-overlay">
    <div class="modal-card">
        <h2 class="modal-title">Confirm Details</h2>
        <p class="modal-content">
          Account Name: <span>{{ formData.account_name }}</span>
        </p>
        <p class="modal-content">
          Type: <span>{{ formData.account_type }}</span>
        </p>
        <p class="modal-content">
          Currency: <span>{{ formData.currency }}</span>
        </p>
        <p class="modal-content">
          Business Registration Number: <span>{{ formData.id_no }}</span>
        </p>
        <div v-if="!isProcessing" class="modal-buttons">
          <button class="modal-btn confirm" @click="confirmTransfer">Yes</button>
          <button class="modal-btn cancel" @click="cancelTransfer">Cancel</button>
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
import utils from "../../utils/utils";
/*import Account_Signatories from "./signatories.vue"; will work on this feature later*/
import Terms_Conditions from "../../components/account_opening/terms_and_conditions.vue";

const url = "http://127.0.0.1:8000/post/open_corporate_account";

export default {
  name: "Corporate_Account",
  data() {
    return {
      formData: {
        account_type: "",
        account_name: "",
        currency: "",
        nationality: "",
        address: "",
        id_no: "",
        kra_pin: "",
        telephone: "",
        email: "",
        dob: "",
        source_of_funds: "",
        annual_income: "",
        intended_usage: "",
      },
      isValidaccount_name: false,
      isValidtelephone: false,
      isValidemail: false,
      isTermsChecked: false,
      isConfirmationVisible: false,
      isProcessing: false,
      showTerms: false,
      tax_cert: null,
      reg_cert: null,
      passport: null,
      signatories: []
    };
  },
  components: { Terms_Conditions },
  methods: {
    async createAccount() {
      try {
        const formData = new FormData();
        formData.append('tax_cert', this.tax_cert);
        formData.append('reg_cert', this.reg_cert);
        formData.append('passport', this.passport);

        const requestBody = utils.generateHmacSignature({
          account_type: this.formData.account_type,
          id_no: this.formData.id_no,
          nationality: this.formData.nationality,
          kra_pin: this.formData.kra_pin,
          account_name: this.formData.account_name,
          address: this.formData.address,
          telephone: this.formData.telephone,
          email: this.formData.email,
          dob: this.formData.dob,
          employment_status: this.formData.employment_status,
          source_of_funds: this.formData.source_of_funds,
          annual_income: this.formData.annual_income,
          intended_usage: this.formData.intended_usage,
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
        this.reg_cert = event.target.files[0]; // Access the selected file
      },
      handleFileUpload3(event) {
        this.passport = event.target.files[0]; // Access the selected file
      },
      toggleTerms() {
        this.showTerms = !this.showTerms;
      },
      showConfirmation() {
        if(!this.isTermsChecked) {
            return
          }
      if (utils.checkEmptyValues(this.formData)) {
        alert("Please fill in all required fields.");
        return;
      }
      this.isConfirmationVisible = true;
    },
    confirmTransfer() {
      this.createAccount();
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
  h1 {
    color: gold;
    margin-left: 5px;

  }
  .success-message {
    color: green;
  }
  .head {
    margin-top: 80px;
  }
  p,
  input,
  select,
  .head {
    margin: 20px;
  }
  label {
    color: white;
    font-size: 15px;
    margin: 20px;
  }
  
  h1, i {
        margin-left: 10px;
        cursor: pointer;
        color: gold;
        position: relative;
  }

.details {
  position: absolute;
  top: 120%;
  left: 50%;
  transform: translateX(-50%);
  background-color: gold;
  padding: 10px;
  border-radius: 5px;
  opacity: 0;
  visibility: hidden;
  transition: 0.3s;
}

h1 i:hover .details,
.details:hover {
  opacity: 1;
  visibility: visible;
}

.info {
  font-size: small;
  color:black;
}

.btn {
  margin-left: 20px;
}
.form-group-dob label {
      display: block;
      margin-bottom: 5px;
      font-weight: bold;
      color: #555;
}
  
.form-group-dob input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  transition: border-color 0.3s;
}
  
.form-group-dob input:focus {
  border-color: #007BFF;
  outline: none;
}
select {
  background-color: rgb(0, 19, 31); color: white; width: 50%;
  border-color: aqua;
}
#annual_income {
  background-color: rgb(0, 19, 31);
  border-radius: 5px;
  border-color: aqua;
  width: 400px;
  color: white;
  height: 40px;
  padding: 5px;
}
legend {
  color: gold;
  margin-left: 20px;
}
h3 {
  font-size: medium;
  color: white;
  margin: 0px 30px 0px 20px
}
#dob {
  color: gold;
  background-color: rgb(0, 19, 31);
  border-radius: 5px;
  border-color: aqua;
  width: 250px;
  height: 50px;
  padding: 20px;
}
.docs {
  color: aqua;
}
</style>
  