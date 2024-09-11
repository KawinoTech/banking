<template>
              <form action="#">
                <label for="account" class="form-label">Choose Account</label>
                  <select id="account" name="account" v-model="formData.account" class="form-select" style="background-color: rgb(0, 19, 31);
                  color: white;width: 50%;">
                  <option v-for="account in all_accounts" :key="account">{{account.account_type}} {{account.currency}}:{{account.account_no}}</option>
                  </select>
                  <div class="form-group">
                    <p v-if="balance > 0 && formData.amount != ''" class="within_limit">Balance: {{balance}}</p>
                    <p v-else-if="balance < 0 && formData.amount != ''" class="exceed_limit">Balance: {{balance}}, Sorry! Insufficient Funds</p>
                  <input type="text" id="amount" name="amount" v-model="formData.amount" placeholder="Enter Amount" @input="check_balance">
                  </div>
                  <div class="form-group">
                  <input type="text" id="beneficiary" name="beneficiary" v-model="formData.beneficiary" placeholder="Enter Beneficiary">
                  </div>
                  <div class="form-group">
                  <textarea id="remarks" name="remarks" v-model="formData.remarks" placeholder="Remarks"></textarea>
                  </div>
                  <div class="form-group">
                  </div>
                  <div class="form-group">
                  <input type="password" id="password" v-model="password" name="password" placeholder="PIN" 
                  style="background-color: rgb(0, 19, 31);
                  border: none;
                  border-bottom: 1px solid aqua;
                  width: 25%;">
                  </div>
                  <button type="button" class="btn btn-success" @click.prevent="transferFunds">Transfer Funds</button>
              </form>
</template>
<script>
const url2 = 'https://sys-audit.tech/post/get_user_accounts'
import check from '../utils/utils'
export default {
    name: "Transfer_Funds",
    data() {
  return {
    formData: {
                  account: '',
                  amount: '',
                  remarks: '',
                  beneficiary: '',
              },
    password: '',
    all_accounts: [],
    balance: ''
          }
      },
      mounted() {
        this.fetchData();
      },
methods: 


{
  findAndReturnSubsequent(str, char) {

    const index = str.indexOf(char);
    if (index !== -1 && index < str.length - 1) {
        return str.substring(index + 1);
    } else {
        return ""; // Character not found or it's the last character
    }
},
    check_balance() {
      if (this.formData.account != '' && this.formData.amount != '')
      {
          for (let i = 0; i < this.all_accounts.length; i++)
            {
                    if(this.findAndReturnSubsequent(this.formData.account, ':') == this.all_accounts[i].account_no)
                    {
                      this.balance = this.all_accounts[i].account_balance - this.formData.amount;
                      
                    }
            }
      }
    },

    async transferFunds() {
      try{
                if (check.checkEmptyValues(this.formData)){
          throw new Error('Empty Fields');
        }
    const response = await fetch('https://sys-audit.tech/post/transfer', {
                                              method: 'POST',
                                              headers: {
                                                'Content-Type': 'application/json',
                                                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                                              },
                                              body: JSON.stringify(
                                                {"amount": Number(this.formData.amount),
                                                "account": this.findAndReturnSubsequent(this.formData.account, ':'),
                                                "remarks": this.formData.remarks,
                                                "beneficiary": this.formData.beneficiary}
                                              )
                                          }
          );
                  if (!response.ok) {
                  throw new Error('Failed to post data');
        }
                setTimeout(() => {
          this.$router.push('/success');
        }, 2000);
        }
        catch (error) {
        console.error('Error posting data:', error);
        setTimeout(() => {
          this.$router.push('/error');
        }, 2000);
        // Handle error if necessary
      }
    },

async fetchData() { 
try {
const response = await fetch(url2,
  {method: 'GET',
                                                  headers: {
                                                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                                                  }
                                              }
);
const data = await response.json();
for (let i = 0; i < data.length; i++)
{
    this.all_accounts.push(data[i]);
}
this.loading = false;
} catch (error) {
console.error('Error fetching data:', error);
}
}
}
}
</script>
<style scoped>
label {
  color: antiquewhite;
  margin-left: 20px;
}
.within_limit {
  margin-top: 10px;
  color: green;
}
.exceed_limit {
  margin-top: 10px;
  color: red;
}
</style>
