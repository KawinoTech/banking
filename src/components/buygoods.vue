<template>
<div>
        <form action="#">
            <div class="form-group">
            <input v-model="formData.amount" type="text" id="amount" name="amount" placeholder="Enter Amount">
            </div>
            <div class="form-group">
            <input v-model="formData.store_no" type="text" id="store_no" name="store_no" placeholder="Store Number">
            </div>
            <div class="form-group">
            <textarea v-model="formData.remarks" id="remarks" name="remarks" placeholder="Remarks"></textarea>
            </div>
            <div class="form-group">

            <select v-model="formData.account" id="account" name="account" class="form-select" style="background-color: rgb(0, 19, 31);
            color: white;width: 50%;">
            <option selected>Select Account to debit</option>
            <option v-for="account in all_accounts" :key="account">{{account.account_type}} {{account.currency}}:{{account.account_no}}</option>
            </select>
            </div>
            <div class="form-group">
            <input v-model="formData.password" type="password" id="password" name="password" placeholder="PIN" 
            style="background-color: rgb(0, 19, 31);
            border: none;
            border-bottom: 1px solid aqua;
            width: 25%;">
            </div>
            <button type="button" class="btn btn-success" @click.prevent="buyGoods">Buy Goods</button>
        </form>
</div>
</template>
<script>
import check from '../utils/utils'
const url2 = 'https://sys-audit.tech/post/get_user_accounts'
export default {
    name: 'Buy_goods',
    data() {
return {
formData: {
            amount: '',
            beneficiary: '',
            remarks: '',
            store_no: '',
            account: '',
            password: ''
        },

all_accounts: []
    }
},



mounted() {
    this.fetchData();
},

methods: {
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
},

  findAndReturnSubsequent(str, char) {
    const index = str.indexOf(char);
    if (index !== -1 && index < str.length - 1) {
        return str.substring(index + 1);
    } else {
        return ""; // Character not found or it's the last character
    }
},

    async buyGoods() {
      try{
                if (check.checkEmptyValues(this.formData)){
          throw new Error('Empty Fields');
        }
    const response = await fetch('https://sys-audit.tech/post/buygoods', {
                                              method: 'POST',
                                              headers: {
                                                'Content-Type': 'application/json',
                                                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                                              },
                                              body: JSON.stringify(
                                                {"amount": Number(this.formData.amount),
                                                "account": this.findAndReturnSubsequent(this.formData.account, ':'),
                                                "remarks": this.formData.remarks,
                                                "store_no": this.formData.store_no}
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
    }

}
};
</script>
