<template>
        <Nav_Bar></Nav_Bar>
        <div class="head">
            <p style="color: rgb(196, 186, 186);">Open New Account</p>
        </div>
        <form action="#">
            <div class="form-group">
                <div class="form-group">
                <div class="account_name_checker" v-if="!isValidaccount_name && formData.account_name != ''">
                  <p style="color: red; font-size: 10px; margin-left: 20px;">Account Name MUST lontain at least 3 seperate unique Names</p>
                </div>
                <input v-model="formData.account_name" type="text" id="account_name" name="account_name" placeholder="Account Name" @input="checkAccNameInpu">
                </div>
                <div class="form-group">
                    <div class="account_name_checker" v-if="!isValidaddress && formData.address != ''">
                      <p style="color: red; font-size: 10px; margin-left: 20px;">The Address you have entered is invalid</p>
                    </div>
                <input v-model="formData.address" type="text" id="address" name="address" placeholder="Address" @input="checkAddressInput">
                </div>
                <div class="form-group">
                <input v-model="formData.telephone" type="text" id="telephone" name="telephone" placeholder="Telephone">
                </div>
                <div class="form-group">
                    <div class="account_name_checker" v-if="!isValididnumber && formData.id_no != ''">
                      <p style="color: red; font-size: 10px; margin-left: 20px;">The ID Number invalid</p>
                    </div>
                <input v-model="formData.id_no" type="text" id="id_no" name="id_no" placeholder="ID Number" @input="checkIdnumberInput">
                </div>
                  <div class="form-group">
                    <div class="account_name_checker" v-if="!isValidkrapin && formData.kra_pin != ''">
                      <p style="color: red; font-size: 10px; margin-left: 20px;">The KRA PIN is invalid</p>
                    </div>
                <input v-model="formData.kra_pin" type="text" id="kra_pin" name="kra_pin" placeholder="KRA PIN" @input="checkKRApinInput">
                </div>
                <div class="form-group">
                <input v-model="formData.next_of_kin" type="text" id="next_of_kin" name="next_of_kin" placeholder="Next of Kin">
                </div>
                <label for="account_type" class="form-label">Choose Type of Account</label>
                <select v-model="formData.account_type" id="account_type" name="account_type" class="form-select" style="background-color: rgb(0, 19, 31);
                color: white;width: 50%;">
                <option selected>Select Account to Open</option>
                <option >Pay As You Go</option>
                <option >Savings Account</option>
                <option >Forex Plus</option>
                <option >SME Banking</option>
                <option >Vue Vantage</option>
                </select>
                <label for="currency" class="form-label">Choose Type of Cuurency</label>
                <select v-model="formData.currency" id="currency" name="currency" class="form-select" style="background-color: rgb(0, 19, 31);
                color: white;width: 50%;">
                <option selected>Select Currency</option>
                <option>KES</option>
                <option>EUR</option>
                <option>POUND</option>
                <option>USD</option>
                </select>
                <label for="currency" class="form-label">Nationality</label>
                <select v-model="formData.nationality" id="nationality" name="nationality" class="form-select" style="background-color: rgb(0, 19, 31);
                color: white;width: 50%;">
                <option selected>Select Nationality</option>
                <option>Kenyan</option>
                <option>British</option>
                <option>American</option>
                <option>French</option>
                </select>
            </div>
            <button type="button" class="btn btn-success" @click.prevent="createAccount">Open Account</button>
        </form>
</template>
<script>
import json from '../assets/types.json'
import Nav_Bar from '../components/navbar.vue'
import check from '../utils/utils'
const url = 'https://sys-audit.tech/post/open_new_account'
export default {
    name: "New_Account",
    components: {
      Nav_Bar
},
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
all_accounts: []
    }
},

mounted() {
    this.fetchJson();
},

methods: {
   fetchJson() {
try {
        for (let i = 0; i < json.accounts.length; i++)
        {
            this.all_accounts.push(json.accounts[i]);
        }
        this.loading = false;
    } 
    catch (error) 
    {
    console.error('Error fetching data:', error);
    }
            },
async createAccount() {
      try {
        if (check.checkEmptyValues(this.formData)){
          throw new Error('Empty Fields');
        }
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
          },
          body: JSON.stringify(this.formData)
        });
        if (!response.ok) {
          throw new Error('Failed to post data');
        }

        // Set success to true after successful post
        this.success = true;
        // Redirect to homepage after 2 seconds
        setTimeout(() => {
          this.$router.push('/success');
        }, 2000);
      } catch (error) {
        console.error('Error posting data:', error);
        setTimeout(() => {
          this.$router.push('/error');
        }, 2000);
        // Handle error if necessary
      }
    },

    checkAccNameInput() {

      if (this.formData.account_name != "Hello")
      {
        this.isValidaccount_name = false;
      }
      else{
        this.isValidaccount_name = true;
      }
    },

        checkAddressInput() {
      if (this.formData.address != "Hello")
      {
        this.isValidaddress = false;
      }
      else{
        this.isValidaddress = true;
      }
    },

            checkIdnumberInput() {
      if (this.formData.id_no != "Hello")
      {
        this.isValididnumber = false;
      }
      else{
        this.isValididnumber = true;
      }
    },

            checkKRApinInput() {
      if (this.formData.kra_pin != "Hello")
      {
        this.isValidkrapin = false;
      }
      else{
        this.isValidkrapin = true;
      }
    }

  }
}
</script>

<style scoped>
.success-message {
  color: green;
}

head {
    display: flex;
    justify-content: center;
    align-items: center;
}
p, label {
    color: rgb(196, 186, 186);
    font-size: 30px;
}

input, select, .head{
  margin: 20px;
}

label {
    color: rgb(118, 106, 106);
    font-size: 15px;
    margin: 20px;
}
</style>
