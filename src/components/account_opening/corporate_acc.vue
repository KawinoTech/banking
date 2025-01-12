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
          <input v-model="formData.account_name" type="text" id="account_name" name="account_name" placeholder="Account Name" @input="checkAccNameInput" />
          <div v-if="!isValidaccount_name && formData.account_name" class="error-message">
            Account Name MUST contain at least 3 unique names
          </div>
        </div>
  
        <div class="form-group">
          <label for="dob">Date of Birth/Incorporation</label>
          <input v-model="formData.dob" type="date" id="dob" name="dob" required />
        </div>
  
        <div class="form-group">
          <label for="residential_address">Residential Address</label>
          <input v-model="formData.residential_address" type="text" id="residential_address" name="residential_address" placeholder="Residential Address" @input="checkAddressInput" />
        </div>
  
        <div class="form-group">
          <label for="telephone">Telephone</label>
          <input v-model="formData.telephone" type="text" id="telephone" name="telephone" placeholder="Telephone" />
        </div>
  
        <div class="form-group">
          <label for="email">Email Address</label>
          <input v-model="formData.email" type="email" id="email" name="email" placeholder="example@domain.com" required />
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
  
      <!-- Identification Details -->
      <fieldset>
        <legend>Identification</legend>
        <div class="form-group">
          <label for="id_no">National ID Number</label>
          <input v-model="formData.id_no" type="text" id="id_no" name="id_no" placeholder="National ID Number" @input="checkIdnumberInput" />
          <div v-if="!isValididnumber && formData.id_no" class="error-message">
            The ID Number is invalid
          </div>
        </div>
  
        <div class="form-group">
          <label for="kra_pin">KRA PIN</label>
          <input v-model="formData.kra_pin" type="text" id="kra_pin" name="kra_pin" placeholder="KRA PIN" @input="checkKRApinInput" />
          <div v-if="!isValidkrapin && formData.kra_pin" class="error-message">
            The KRA PIN is invalid
          </div>
        </div>
  
        <div class="form-group">
          <label for="nssf_no">NSSF Number</label>
          <input v-model="formData.nssf_no" type="text" id="nssf_no" name="nssf_no" placeholder="NSSF Number" required />
          <div v-if="!isValidnssf && formData.nssf_no" class="error-message">
            The NSSF number is invalid
          </div>
        </div>
      </fieldset>
  
      <!-- Employment and Financial Details -->
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
          <input v-model="formData.annual_income" type="number" id="annual_income" name="annual_income" placeholder="Enter Annual Income" required />
        </div>
  
        <div class="form-group">
          <label for="usage">Purpose of Account</label>
          <input v-model="formData.intended_usage" type="text" id="usage" name="usage" placeholder="E.g., Online shopping, travel" />
        </div>
      </fieldset>
  
      <!-- Next of Kin Details -->
      <fieldset>
        <legend>Next of Kin</legend>
        <div class="form-group">
          <label for="next_of_kin">Name</label>
          <input v-model="formData.next_of_kin" type="text" id="next_of_kin" name="next_of_kin" placeholder="Next of Kin" />
        </div>
  
        <div class="form-group">
          <label for="relationship">Relationship</label>
          <select v-model="formData.relationship" id="relationship" name="relationship">
            <option value="" disabled selected>Select Relationship</option>
            <option>Parent</option>
            <option>Sibling</option>
            <option>Relative</option>
          </select>
        </div>
      </fieldset>
  
      <!-- Account Details -->
      <fieldset>
        <legend>Account Details</legend>
        <div class="form-group">
          <label for="account_type">Account Type</label>
          <select v-model="formData.account_type" id="account_type" name="account_type" required>
            <option value="" disabled selected>Select Account Type</option>
            <option>Pay As You Go</option>
            <option>Savings Account</option>
            <option>Forex Plus</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="currency">Currency</label>
          <select v-model="formData.currency" id="currency" name="currency" required>
            <option value="" disabled selected>Select Currency</option>
            <option>KES</option>
            <option>EUR</option>
            <option>POUND</option>
            <option>USD</option>
          </select>
        </div>
  
      </fieldset>
      <fieldset>
        <legend>Documentation</legend>
        <div>
          <h3 style="display: inline;">Tax compliance</h3>
            <input type="file" @change="handleFileUpload" />
        </div>
        <div>
          <h3 style="display: inline;">National ID</h3>
            <input type="file" @change="handleFileUpload" />
        </div>
        <div>
          <h3 style="display: inline;">Passport photo</h3>
            <input type="file" @change="handleFileUpload" />
        </div>
      </fieldset>
  
      <!-- Terms and Conditions -->
      <div class="form-group">
        <label class="terms">
          <input type="checkbox" name="terms" required />
          I agree to the terms and conditions.
        </label>
      </div>
  
      <button type="button" class="btn btn-success" @click.prevent="createAccount">Open Account</button>
    </form>
  </template>
  
  
  <script>
  import check from '../../utils/utils';
  
  const url = 'http://127.0.0.1:8000/post/open_new_account';
  
  export default {
    name: 'Corporate_Account',
    data() {
      return {
        formData: {
          account_type: '',
          account_name: '',
          currency: '',
          residential_address: '',
          id_no: '',
          nationality: '',
          kra_pin: '',
          telephone: '',
          next_of_kin: '',
          email: '',
          dob: '',
          nssf_no: '',
          employment_status: '',
          source_of_funds: '',
          annual_income: '',
          intended_usage: '',
          relationship: ''
        },
        loading: true,
        isValidaccount_name: false,
        isValidaddress: true,
        isValididnumber: true,
        isValidkrapin: true,
        isTandCsclicked: false,
        selectedFile: null,
      };
    },
  
    methods: {
      async createAccount() {
        try {
          if (check.checkEmptyValues(this.formData)) {
            throw new Error('Empty Fields');
          }
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('accessToken')}`
            },
            body: JSON.stringify(this.formData)
          });
          if (!response.ok) {
            throw new Error('Failed to post data');
          }
          this.success = true;
          setTimeout(() => this.$router.push('/success'), 2000);
        } catch (error) {
          console.error('Error posting data:', error);
          setTimeout(() => this.$router.push('/error'), 2000);
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
      checkAddressInput() {
        this.isValidaddress = this.formData.address === 'Hello';
      },
      checkIdnumberInput() {
        this.isValididnumber = this.formData.id_no === 'Hello';
      },
      checkKRApinInput() {
        this.isValidkrapin = this.formData.kra_pin === 'Hello';
      },
      handleFileUpload(event) {
        this.selectedFile = event.target.files[0]; // Access the selected file
      }
    }
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
  
  /* Style the details area */
  .details {
    position: absolute;
    top: 120%; /* Position below the icon */
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
  
  /* Show details when hovering over the icon or details */
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
  </style>
  