<template>
  <div>
    <!-- Page Header -->
    <h1>
      Open Personal Account
      <i class="fa-solid fa-circle-question">
        <div class="details">
          <router-link to="/instructions_on_opening_transactional_account">
            <p class="info">Click to find details on account opening</p>
          </router-link>
        </div>
      </i>
    </h1>

    <!-- Account Form -->
    <form action="#" class="account-form">
      <!-- Personal Information Section -->
      <fieldset>
        <legend>Personal Information</legend>
        
        <div class="form-group">
          <label for="account_name">Account Name</label>
          <input
            v-model="formData.account_name"
            type="text"
            id="account_name"
            name="account_name"
            placeholder="Account Name"
            @input="checkAccNameInput"
          />
          <div v-if="!isValidaccount_name && formData.account_name" class="error-message">
            Account Name MUST contain at least 3 unique names
          </div>
        </div>

        <div class="form-group">
          <label for="account_type">Account Type</label>
          <select v-model="formData.account_type" id="account_type" name="account_type" required>
            <option value="" disabled selected>Select Account Type</option>
            <option>Pay As You Go</option>
            <option>Savings Account</option>
          </select>
        </div>

        <div class="form-group">
          <label for="dob">Date of Birth/Incorporation</label>
          <input v-model="formData.dob" type="date" id="dob" name="dob" required />
        </div>

        <div class="form-group">
          <label for="address">Residential Address</label>
          <input
            v-model="formData.address"
            type="text"
            id="address"
            name="address"
            placeholder="Residential Address"
          />
        </div>

        <div class="form-group">
          <label for="telephone">Telephone</label>
          <input
            v-model="formData.telephone"
            type="text"
            id="telephone"
            name="telephone"
            placeholder="Telephone"
            @input="checkTelephoneInput"
          />
          <div v-if="!isValidtelephone && formData.telephone" class="error-message">
            Incorrect format
          </div>
        </div>

        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            v-model="formData.email"
            type="email"
            id="email"
            name="email"
            placeholder="example@domain.com"
            @input="checkEmailInput"
            required
          />
          <div v-if="!isValidemail && formData.email" class="error-message">
            Incorrect format
          </div>
        </div>

        <div class="form-group">
          <label for="nationality">Nationality</label>
          <select v-model="formData.nationality" id="nationality" name="nationality" required>
            <option value="" disabled selected>Select Nationality</option>
            <option>Kenyan</option>
            <option>British</option>
            <option>American</option>
            <option>French</option>
          </select>
        </div>
      </fieldset>

      <!-- Identification Details Section -->
      <fieldset>
        <legend>Identification</legend>
        
        <div class="form-group">
          <label for="id_no">National ID Number</label>
          <input
            v-model="formData.id_no"
            type="text"
            id="id_no"
            name="id_no"
            placeholder="National ID Number"
          />
        </div>

        <div class="form-group">
          <label for="kra_pin">KRA PIN</label>
          <input
            v-model="formData.kra_pin"
            type="text"
            id="kra_pin"
            name="kra_pin"
            placeholder="KRA PIN"
          />
        </div>

        <div class="form-group">
          <label for="nssf_no">NSSF Number</label>
          <input
            v-model="formData.nssf_no"
            type="text"
            id="nssf_no"
            name="nssf_no"
            placeholder="NSSF Number"
            required
          />
        </div>
      </fieldset>

      <!-- Employment and Financial Details Section -->
      <fieldset>
        <legend>Employment and Financial Details</legend>
        
        <div class="form-group">
          <label for="employment_status">Employment Status</label>
          <select v-model="formData.employment_status" id="employment_status" name="employment_status" required>
            <option value="" disabled selected>Select Employment Status</option>
            <option value="employed">Employed</option>
            <option value="self-employed">Self-Employed</option>
            <option value="student">Student</option>
            <option value="unemployed">Unemployed</option>
            <option value="business">Business</option>
          </select>
        </div>

        <div class="form-group">
          <label for="source_of_funds">Source of Funds</label>
          <select v-model="formData.source_of_funds" id="source_of_funds" name="source_of_funds" required>
            <option value="" disabled selected>Select Source of Funds</option>
            <option>Salary</option>
            <option>Business Income</option>
            <option>Inheritance</option>
          </select>
        </div>

        <div class="form-group">
          <label for="annual_income">Annual Income (KES)</label>
          <input
            v-model="formData.annual_income"
            type="number"
            id="annual_income"
            name="annual_income"
            placeholder="Enter Annual Income"
            required
          />
        </div>

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

      <!-- Next of Kin Section -->
      <fieldset>
        <legend>Next of Kin</legend>

        <div class="form-group">
          <label for="next_of_kin">Name</label>
          <input
            v-model="formData.next_of_kin"
            type="text"
            id="next_of_kin"
            name="next_of_kin"
            placeholder="Next of Kin"
          />
        </div>

        <div class="form-group">
          <label for="next_of_kin_id">National ID/Passport Number</label>
          <input
            v-model="formData.next_of_kin_id"
            type="text"
            id="next_of_kin_id"
            name="next_of_kin_id"
            placeholder="National ID/Passport Number"
          />
        </div>

        <div class="form-group">
          <label for="nok_relationship">Relationship</label>
          <select v-model="formData.nok_relationship" id="nok_relationship" name="nok_relationship">
            <option value="" disabled selected>Select Relationship</option>
            <option>Parent</option>
            <option>Sibling</option>
            <option>Relative</option>
          </select>
        </div>
      </fieldset>

      <!-- Documentation Section -->
      <fieldset>
        <legend>Documentation</legend>
        
        <div>
          <h3 style="display: inline;">Tax Compliance</h3>
          <input class="docs" type="file" @change="handleFileUpload1" />
        </div>

        <div>
          <h3 style="display: inline;">National ID</h3>
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
        <p id="tandc" style="color: green;">
          Terms and Conditions {{ isTermsChecked ? 'checked' : 'unchecked' }}
        </p>
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
            Telephone: <span>{{ formData.telephone }}</span>
          </p>
          <p class="modal-content-">
            Email: <span>{{ formData.email }}</span>
          </p>

          <div v-if="!isProcessing" class="modal-buttons-">
            <button class="modal-btn- confirm" @click="confirmTransfer">Yes</button>
            <button class="modal-btn- cancel" @click="cancelTransfer">Cancel</button>
          </div>
          <div v-if="isProcessing">
            <p class="wait">Processing<i class="fa-regular wait fa-clock fa-spin"></i></p>
          </div>
        </div>
    </div>
  </div>
</template>


<script>
import utils from '../../utils/utils';
import Terms_Conditions from '../../components/account_opening/terms_and_conditions.vue';

// The URL endpoint for creating a personal account
import apiEndpoints from '@/api/apiEndpoints';

export default {
  name: 'Personal_Account',
  components: {
    Terms_Conditions,
  },
  data() {
    /**
     * Data properties for managing form inputs, validation, and UI state.
     */
    return {
      // Form data fields
      formData: {
        account_type: '',        // Type of account (e.g., Savings, Pay As You Go)
        account_name: '',        // Account holder's name
        id_no: '',               // National ID number
        nationality: '',         // Nationality of the account holder
        kra_pin: '',             // KRA PIN for tax purposes
        telephone: '',           // Telephone number in international format
        next_of_kin: '',         // Name of next of kin
        next_of_kin_id: '',      // ID or passport number of next of kin
        email: '',               // Email address
        dob: '',                 // Date of birth or incorporation
        nssf_no: '',             // NSSF number
        employment_status: '',   // Employment status (e.g., employed, student)
        source_of_funds: '',     // Source of account funding
        address: '',             // Residential address
        annual_income: '',       // Annual income in KES
        intended_usage: '',      // Purpose of the account
        nok_relationship: '',    // Relationship with next of kin
      },
      isValidaccount_name: false, // Validation flag for account name
      isValidtelephone: false,   // Validation flag for telephone number
      isValidemail: false,       // Validation flag for email
      isTermsChecked: false,     // Whether terms and conditions are accepted
      isConfirmationVisible: false, // Confirmation modal visibility
      isProcessing: false,       // State of account creation process
      tax_cert: null,            // Uploaded tax compliance certificate
      reg_cert: null,            // Uploaded registration certificate
      passport: null,            // Uploaded passport photo
      showTerms: false,          // Terms and conditions visibility
    };
  },
  methods: {
    /**
     * Sends a POST request to create a personal account with the provided form data and documents.
     * Handles both success and error scenarios.
     */
    async createAccount() {
      try {
        // Prepare form data for submission
        const formData = new FormData();
        formData.append('tax_cert', this.tax_cert);
        formData.append('reg_cert', this.reg_cert);
        formData.append('passport', this.passport);

        // Generate HMAC signature for security
        const requestBody = utils.generateHmacSignature({
          account_type: this.formData.account_type,
          nationality: this.formData.nationality,
          id_no: this.formData.id_no,
          kra_pin: this.formData.kra_pin,
          account_name: this.formData.account_name,
          address: this.formData.address,
          telephone: this.formData.telephone,
          next_of_kin: this.formData.next_of_kin,
          email: this.formData.email,
          dob: this.formData.dob,
          nssf_no: this.formData.nssf_no,
          employment_status: this.formData.employment_status,
          source_of_funds: this.formData.source_of_funds,
          annual_income: this.formData.annual_income,
          intended_usage: this.formData.intended_usage,
          nok_relationship: this.formData.nok_relationship,
          next_of_kin_id: this.formData.next_of_kin_id,
        });

        // Append payload and signature to form data
        formData.append('signature', requestBody['signature']);
        formData.append('payload', JSON.stringify(requestBody['payload']));

        // Submit form data to the server
        const response = await fetch(apiEndpoints.accounts.openPersonalAccount, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Failed to post data');
        }

        // Redirect to success page upon successful account creation
        this.success = true;
        setTimeout(() => this.$router.push('/success'), 2000);
      } catch (error) {
        console.error('Error posting data:', error);

        // Redirect to failure page upon error
        setTimeout(() => this.$router.push('/failed'), 500);
      }
    },

    /**
     * Validates the account name format (e.g., First Middle Last with capitalization).
     */
    checkAccNameInput() {
      const namePattern = /^[A-Z][a-z]* [A-Z][a-z]* [A-Z][a-z]*$/;
      this.isValidaccount_name = namePattern.test(this.formData.account_name);
    },

    /**
     * Validates the telephone number format (e.g., +123 123456789).
     */
    checkTelephoneInput() {
      const namePattern = /^\+\d{1,3}\s\d{9}$/;
      this.isValidtelephone = namePattern.test(this.formData.telephone);
    },

    /**
     * Validates the email address format.
     */
    checkEmailInput() {
      const namePattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      this.isValidemail = namePattern.test(this.formData.email);
    },

    /**
     * Toggles the visibility of terms and conditions.
     */
    toggleTerms() {
      this.showTerms = !this.showTerms;
    },

    /**
     * Handles file upload for tax compliance certificate.
     */
    handleFileUpload1(event) {
      this.tax_cert = event.target.files[0];
    },

    /**
     * Handles file upload for registration certificate.
     */
    handleFileUpload2(event) {
      this.reg_cert = event.target.files[0];
    },

    /**
     * Handles file upload for passport photo.
     */
    handleFileUpload3(event) {
      this.passport = event.target.files[0];
    },

    /**
     * Initiates the account creation process and shows a processing state.
     */
    confirmTransfer() {
      this.createAccount();
      this.isProcessing = true;
    },

    /**
     * Cancels the account creation process and hides the confirmation modal.
     */
    cancelTransfer() {
      this.isConfirmationVisible = false;
    },

    /**
     * Displays the confirmation modal after validating terms acceptance and form completeness.
     */
    showConfirmation() {
      if (!this.isTermsChecked) {
        alert('Please check the Terms and Conditions');
        return;
      }
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


label {
  color: rgb(196, 186, 186);
  font-size: 30px;
}

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

h1 i {
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
  border: 1px solid;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
  z-index: 1000;
}

h1 i:hover .details,
.details:hover {
  opacity: 1;
  visibility: visible;
}

.info {
  font-size: small;
  color: black;
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
  background-color: rgb(0, 19, 31);
  color: white;
  width: 50%;
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
  margin: 0px 30px 0px 20px;
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
#tandc {
  font-size: medium;
  margin: 20px;
}
span {
  color: green;
}
.wait {
  color: white;
}
</style>
