<template>
  <Nav_Bar></Nav_Bar>
  <h1>
    Open New Account
    <i class="fa-solid fa-circle-question">
      <div class="details"><router-link to="/instructions_on_opening_transactional_account"><p class="info">Click to find details on account opening</p></router-link></div>
    </i>
  </h1>
  <form action="#">
    <div class="form-group">
      <!-- Account Name -->
      <div class="form-group">
        <div v-if="!isValidaccount_name && formData.account_name != ''" class="account_name_checker">
          <p style="color: red; font-size: 10px; margin-left: 20px;">
            Account Name MUST contain at least 3 separate unique names
          </p>
        </div>
        <input v-model="formData.account_name" 
               type="text" 
               id="account_name" 
               name="account_name" 
               placeholder="Account Name" 
               @input="checkAccNameInput" />
      </div>

      <!-- Address -->
      <div class="form-group">
        <div v-if="!isValidaddress && formData.address != ''" class="account_name_checker">
          <p style="color: red; font-size: 10px; margin-left: 20px;">
            The Address you have entered is invalid
          </p>
        </div>
        <input v-model="formData.address" 
               type="text" 
               id="address" 
               name="address" 
               placeholder="Address" 
               @input="checkAddressInput" />
      </div>

      <!-- Telephone -->
      <div class="form-group">
        <input v-model="formData.telephone" 
               type="text" 
               id="telephone" 
               name="telephone" 
               placeholder="Telephone" />
      </div>

      <!-- ID Number -->
      <div class="form-group">
        <div v-if="!isValididnumber && formData.id_no != ''" class="account_name_checker">
          <p style="color: red; font-size: 10px; margin-left: 20px;">
            The ID Number is invalid
          </p>
        </div>
        <input v-model="formData.id_no" 
               type="text" 
               id="id_no" 
               name="id_no" 
               placeholder="ID Number" 
               @input="checkIdnumberInput" />
      </div>

      <!-- KRA PIN -->
      <div class="form-group">
        <div v-if="!isValidkrapin && formData.kra_pin != ''" class="account_name_checker">
          <p style="color: red; font-size: 10px; margin-left: 20px;">
            The KRA PIN is invalid
          </p>
        </div>
        <input v-model="formData.kra_pin" 
               type="text" 
               id="kra_pin" 
               name="kra_pin" 
               placeholder="KRA PIN" 
               @input="checkKRApinInput" />
      </div>

      <!-- Next of Kin -->
      <div class="form-group">
        <input v-model="formData.next_of_kin" 
               type="text" 
               id="next_of_kin" 
               name="next_of_kin" 
               placeholder="Next of Kin" />
      </div>

      <!-- Account Type -->
      <label for="account_type" class="form-label">Choose Type of Account</label>
      <select v-model="formData.account_type" 
              id="account_type" 
              name="account_type" 
              class="form-select" 
              style="background-color: rgb(0, 19, 31); color: white; width: 50%;">
        <option selected>Select Account to Open</option>
        <option>Pay As You Go</option>
        <option>Savings Account</option>
        <option>Forex Plus</option>
        <option>SME Banking</option>
        <option>Vue Vantage</option>
      </select>

      <!-- Currency -->
      <label for="currency" class="form-label">Choose Type of Currency</label>
      <select v-model="formData.currency" 
              id="currency" 
              name="currency" 
              class="form-select" 
              style="background-color: rgb(0, 19, 31); color: white; width: 50%;">
        <option selected>Select Currency</option>
        <option>KES</option>
        <option>EUR</option>
        <option>POUND</option>
        <option>USD</option>
      </select>

      <!-- Nationality -->
      <label for="nationality" class="form-label">Nationality</label>
      <select v-model="formData.nationality" 
              id="nationality" 
              name="nationality" 
              class="form-select" 
              style="background-color: rgb(0, 19, 31); color: white; width: 50%;">
        <option selected>Select Nationality</option>
        <option>Kenyan</option>
        <option>British</option>
        <option>American</option>
        <option>French</option>
      </select>
    </div>

    <label class="terms">
        <input type="checkbox" name="terms" required>
        I agree to the terms and conditions.
      </label>

    <button type="button" class="btn btn-success" @click.prevent="createAccount">Open Account</button>
  </form>
</template>

<script>
import json from '../../assets/types.json';
import Nav_Bar from '../../components/navbar.vue';
import check from '../../utils/utils';

const url = 'http://127.0.0.1:8000/post/open_new_account';

export default {
  name: 'New_Account',
  components: { Nav_Bar },
  data() {
    return {
      formData: {
        account_type: '',
        account_name: '',
        currency: '',
        address: '',
        id_no: '',
        nationality: '',
        kra_pin: '',
        telephone: '',
        next_of_kin: ''
      },
      loading: true,
      isValidaccount_name: true,
      isValidaddress: true,
      isValididnumber: true,
      isValidkrapin: true,
      all_accounts: [],
      isTandCsclicked: false,
    };
  },
  mounted() {
    this.fetchJson();
  },
  methods: {
    fetchJson() {
      try {
        json.accounts.forEach(account => {
          this.all_accounts.push(account);
        });
        this.loading = false;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
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
      this.isValidaccount_name = this.formData.account_name === 'Hello';
    },
    checkAddressInput() {
      this.isValidaddress = this.formData.address === 'Hello';
    },
    checkIdnumberInput() {
      this.isValididnumber = this.formData.id_no === 'Hello';
    },
    checkKRApinInput() {
      this.isValidkrapin = this.formData.kra_pin === 'Hello';
    }
  }
};
</script>

<style scoped>
h1 {
  color: gold;
  margin-left: 5px;
  margin-top: 80px;
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
</style>
