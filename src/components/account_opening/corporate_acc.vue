<template>
  <!-- Main Title -->
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

  <!-- Account Opening Form -->
  <form action="#" class="account-form">
    <!-- Personal Information Section -->
    <fieldset>
      <legend>Personal Information</legend>

      <!-- Account Name -->
      <div class="form-group">
        <label for="account_name">Account Name</label>
        <div v-if="!isValidaccount_name && formData.account_name" class="error-message">
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

      <!-- Date of Incorporation -->
      <div class="form-group">
        <label for="dob">Date of Incorporation</label>
        <input v-model="formData.dob" type="date" id="dob" name="dob" required />
      </div>

      <!-- Business Nationality -->
      <div class="form-group">
        <label for="address">Business Nationality</label>
        <input v-model="formData.nationality" type="text" id="nationality" name="nationality" placeholder="Business Nationality" />
      </div>

      <!-- Premise Address -->
      <div class="form-group">
        <label for="address">Premise Address</label>
        <input v-model="formData.address" type="text" id="address" name="address" placeholder="Premise Address" />
      </div>

      <!-- Telephone -->
      <div class="form-group">
        <label for="telephone">Telephone</label>
        <div v-if="!isValidtelephone && formData.telephone" class="error-message">
          Incorrect format
        </div>
        <input
          @input="checkTelephoneInput"
          v-model="formData.telephone"
          type="text"
          id="telephone"
          name="telephone"
          placeholder="Telephone"
        />
      </div>

      <!-- Email Address -->
      <div class="form-group">
        <label for="email">Email Address</label>
        <div v-if="!isValidemail && formData.email" class="error-message">
          Incorrect format
        </div>
        <input
          @input="checkEmailInput"
          v-model="formData.email"
          type="email"
          id="email"
          name="email"
          placeholder="example@domain.com"
          required
        />
      </div>
    </fieldset>

    <!-- Identification Section -->
    <fieldset>
      <legend>Identification</legend>

      <!-- Company Registration Number -->
      <div class="form-group">
        <label for="id_no">Company Registration Number</label>
        <input v-model="formData.id_no" type="text" id="id_no" name="id_no" placeholder="Company Registration Number" />
      </div>

      <!-- KRA PIN -->
      <div class="form-group">
        <label for="kra_pin">KRA PIN</label>
        <input v-model="formData.kra_pin" type="text" id="kra_pin" name="kra_pin" placeholder="KRA PIN" />
      </div>
    </fieldset>

    <!-- Financial Details Section -->
    <fieldset>
      <legend>Financial Details</legend>

      <!-- Source of Funds -->
      <div class="form-group">
        <label for="source_of_funds">Source of Funds</label>
        <input
          v-model="formData.source_of_funds"
          type="text"
          id="usage"
          name="usage"
          placeholder="E.g., Farming, Sales"
        />
      </div>

      <!-- Annual Turnover -->
      <div class="form-group">
        <label for="annual_income">Annual Turnover (KES)</label>
        <input
          v-model="formData.annual_income"
          type="number"
          id="annual_income"
          name="annual_income"
          placeholder="Enter Annual Income"
          required
        />
      </div>

      <!-- Purpose of Account -->
      <div class="form-group">
        <label for="usage">Purpose of Account</label>
        <input
          v-model="formData.intended_usage"
          type="text"
          id="usage"
          name="usage"
          placeholder="E.g., Online shopping, travel"
        />
      </div>
    </fieldset>

    <!-- Account Details Section -->
    <fieldset>
      <legend>Account Details</legend>

      <!-- Account Type -->
      <div class="form-group">
        <label for="account_type">Account Type</label>
        <select v-model="formData.account_type" id="account_type" name="account_type" required>
          <option value="" disabled selected>Select Account Type</option>
          <option>Vue Vantage</option>
          <option>SME Banking</option>
          <option>Vue Corporate</option>
        </select>
      </div>

      <!-- Currency -->
      <div class="form-group">
        <label for="currency">Currency</label>
        <select v-model="formData.currency" id="currency" name="currency" required>
          <option value="" disabled selected>Select Currency</option>
          <option>KES</option>
        </select>
      </div>
    </fieldset>

    <!-- Documentation Section -->
    <fieldset>
      <legend>Documentation</legend>

      <!-- Tax Compliance -->
      <div>
        <h3 style="display: inline;">Tax Compliance</h3>
        <input class="docs" type="file" @change="handleFileUpload1" />
      </div>

      <!-- Business Registration Certificate -->
      <div>
        <h3 style="display: inline;">Business Registration Certificate</h3>
        <input class="docs" type="file" @change="handleFileUpload2" />
      </div>

      <!-- Passport Photo -->
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

    <!-- Submit Button -->
    <button type="button" class="btn btn-success" @click.prevent="showConfirmation">
      Open Account
    </button>
  </form>

  <!-- Terms and Conditions Modal -->
  <div v-if="showTerms" class="overlay">
    <div class="terms-modal">
      <Terms_Conditions />
      <button class="close-btn" @click="toggleTerms">Close</button>
    </div>
  </div>

  <!-- Confirmation Modal -->
  <div v-if="isConfirmationVisible" class="modal-overlay">
    <div class="modal-card-">
      <h2 class="modal-title-">Confirm Details</h2>
      <p class="modal-content-">
        Account Name: <span>{{ formData.account_name }}</span>
      </p>
      <p class="modal-content-">
        Type: <span>{{ formData.account_type }}</span>
      </p>
      <p class="modal-content-">
        Currency: <span>{{ formData.currency }}</span>
      </p>
      <p class="modal-content-">
        Business Registration Number: <span>{{ formData.id_no }}</span>
      </p>
      <div v-if="!isProcessing" class="modal-buttons-">
        <button class="modal-btn- confirm" @click="confirmTransfer">Yes</button>
        <button class="modal-btn- cancel" @click="cancelTransfer">Cancel</button>
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
/* Import statement for Account Signatories commented out, as it will be worked on later */
// import Account_Signatories from "./signatories.vue"; 
import Terms_Conditions from "../../components/account_opening/terms_and_conditions.vue";

const url = "http://127.0.0.1:8000/post/open_corporate_account";

export default {
  name: "Corporate_Account",
  data() {
    return {
      formData: {
        account_type: "",           // Type of account to open
        account_name: "",           // Name of the corporate account
        currency: "",               // Preferred currency for transactions
        nationality: "",            // Business nationality
        address: "",                // Business address
        id_no: "",                  // Company registration number
        kra_pin: "",                // Tax identification number
        telephone: "",              // Contact telephone number
        email: "",                  // Contact email address
        dob: "",                    // Date of incorporation
        source_of_funds: "",        // Source of funds for the business
        annual_income: "",          // Annual turnover in KES
        intended_usage: "",         // Purpose of the account
      },
      isValidaccount_name: false,   // Validity check for account name
      isValidtelephone: false,     // Validity check for telephone number
      isValidemail: false,         // Validity check for email address
      isTermsChecked: false,       // Boolean for terms acceptance
      isConfirmationVisible: false, // Display state of the confirmation modal
      isProcessing: false,         // State to indicate processing of the form
      showTerms: false,            // State to show/hide terms and conditions modal
      tax_cert: null,              // File input for tax compliance certificate
      reg_cert: null,              // File input for business registration certificate
      passport: null,              // File input for passport photo
      signatories: [],             // Placeholder for future feature: account signatories
    };
  },
  components: { Terms_Conditions },
  methods: {
    // Method to create a corporate account
    async createAccount() {
      try {
        const formData = new FormData();
        formData.append("tax_cert", this.tax_cert);
        formData.append("reg_cert", this.reg_cert);
        formData.append("passport", this.passport);

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

        formData.append("signature", requestBody.signature);
        formData.append("payload", JSON.stringify(requestBody.payload));

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

    // Method to validate account name
    checkAccNameInput() {
      const namePattern = /^[A-Z][a-z]* [A-Z][a-z]* [A-Z][a-z]*$/;
      this.isValidaccount_name = namePattern.test(this.formData.account_name);
    },

    // Method to validate telephone input
    checkTelephoneInput() {
      const telephonePattern = /^\+\d{1,3}\s\d{9}$/;
      this.isValidtelephone = telephonePattern.test(this.formData.telephone);
    },

    // Method to validate email input
    checkEmailInput() {
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      this.isValidemail = emailPattern.test(this.formData.email);
    },

    // Handlers for file uploads
    handleFileUpload1(event) {
      this.tax_cert = event.target.files[0];
    },
    handleFileUpload2(event) {
      this.reg_cert = event.target.files[0];
    },
    handleFileUpload3(event) {
      this.passport = event.target.files[0];
    },

    // Toggles the display of terms and conditions
    toggleTerms() {
      this.showTerms = !this.showTerms;
    },

    // Displays confirmation modal if terms are checked
    showConfirmation() {
      if (!this.isTermsChecked) return;
      if (utils.checkEmptyValues(this.formData)) {
        alert("Please fill in all required fields.");
        return;
      }
      this.isConfirmationVisible = true;
    },

    // Confirms the transfer and processes the account creation
    confirmTransfer() {
      this.createAccount();
      this.isProcessing = true;
    },

    // Cancels the transfer process
    cancelTransfer() {
      this.isConfirmationVisible = false;
    },
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
.wait {
  color: white;
}
</style>
  