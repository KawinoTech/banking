<template>
  <Nav_Bar></Nav_Bar>
    <form action="#">
      <h1>Send Money</h1>
      <label for="account" class="form-label">Choose Account</label>
        <select id="account" 
        name="account"
        v-model="formData.account"
        class="form-select">
          <option v-for="account in all_accounts" :key="account">
            {{account.account_type}} {{account.currency}}:{{account.account_no}}
          </option>
        </select>
        <div class="form-group">
          <p v-if="balance > 0 && formData.amount != ''" class="within_limit">Balance: {{balance}}</p>
            <div class="overdraft" v-else-if="balance < 0 && formData.amount != ''">
              <p class="exceed_limit">Balance: {{balance}}, Sorry! Insufficient Funds</p>
              <button type="button" class="btn btn-success">Request Overdraft</button>
            </div>
            <input type="text"
            id="amount"
            name="amount"
            v-model="formData.amount"
            placeholder="Enter Amount"
            @input="check_balance">
            </div>
            <div class="form-group">
              <input type="text"
              id="beneficiary"
              name="beneficiary"
              v-model="formData.beneficiary"
              placeholder="Enter Beneficiary">
            </div>
            <div class="form-group">
              <textarea
              id="remarks"
              name="remarks"
              v-model="formData.remarks"
              placeholder="Remarks">
              </textarea>
            </div>
            <div class="form-group">
              <input type="password"
              id="password"
              v-model="password"
              name="password"
              placeholder="PIN" 
              style="width: 25%;">
            </div>
            <button type="button" class="btn btn-success" @click="showConfirmation">
              Transfer Funds
            </button>
    </form>
    <div class="modal-overlay" v-if="isConfirmationVisible">
      <div class="modal-card">
        <h2 class="modal-title">Confirm Details</h2>
          <p class="modal-content">Beneficiary: <span>{{ formData.beneficiary }}</span></p>
          <p class="modal-content">Amount: <span>{{ formData.amount }}</span></p>
          <p class="modal-content"> Source Account: <span>{{ formData.account }}</span></p>
          <p class="modal-content"> Description: <span>{{ formData.remarks }}</span></p>
        <div v-if="!isProcessing" class="modal-buttons">
        <button class="modal-btn confirm" @click="confirmTransfer">Yes</button>
        <button class="modal-btn cancel" @click="cancelTransfer">Cancel</button>
        </div>
        <div v-if="isProcessing"><p class="wait">Processing<i class="fa-regular wait fa-clock fa-spin"></i></p></div>
      </div>
    </div>
</template>
<script>
const url2 = 'http://127.0.0.1:8000/post/get_user_accounts'
import Nav_Bar from '../../components/navbar.vue'
import utils from '../../utils/utils'
export default {
    name: "Transfer_Funds",
    components: {
      Nav_Bar,
    },
    data() {
    return {
      formData: {
                    account: '',
                    amount: '',
                    remarks: '',
                    beneficiary: '',
                },
      password: '',
      isConfirmationVisible: false,
      isProcessing: false,
      all_accounts: []
          }
      },
      mounted() {
        this.fetchData();
      },
      methods: {
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
          for (let i = 0; i < this.all_accounts.length; i++) {
              if(this.findAndReturnSubsequent(this.formData.account, ':') == this.all_accounts[i].account_no) {
                this.balance = this.all_accounts[i].account_balance - this.formData.amount;
              }
          }
        }
      },

      showConfirmation() {
        // Validate before showing confirmation
        if (utils.checkEmptyValues(this.formData)) {
          alert('Please fill in all required fields.');
          return;
        }
        this.isConfirmationVisible = true;
      },

      confirmTransfer() {
        this.transferFunds();
        this.isProcessing = true;
      },

      cancelTransfer() {
        this.isConfirmationVisible = false;
      },

      async transferFunds() {
      try{
          if (utils.checkEmptyValues(this.formData)){
            throw new Error('Empty Fields');
      }
      const requestBody = utils.generateHmacSignature( {"amount": Number(this.formData.amount),
                          "account": this.findAndReturnSubsequent(this.formData.account, ':'),
                          "remarks": this.formData.remarks,
                          "beneficiary": this.formData.beneficiary})
      const response = await fetch('http://127.0.0.1:8000/post/transfer', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                        },
                        body: JSON.stringify(requestBody)
                        }
                       );
      if (!response.ok) {
      throw new Error('Failed to post data');
      }
      setTimeout(() => {
            this.isConfirmationVisible = false;
            this.isProcessing = false;
            this.$router.push('/success');
          }, 3000);
         }
         catch (error) {
            console.error('Error posting data:', error);
            setTimeout(() => {
              this.isConfirmationVisible = false;
              this.isProcessing = false;
              this.$router.push('/error');
            }, 1000);
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
      } 
      catch (error) {
        console.error('Error fetching data:', error);
    }
  }
  }
}
</script>
<style scoped>
h1 {
  color: gold; margin-left: 5px;
}
label {
  color: antiquewhite;
  margin-left: 20px;
}
form {
  margin-left: 10px;
  margin-top: 80px
}

span {
  color: green;
}

select {
  background-color: rgb(0, 19, 31);
  color: white; 
  width: 50%;
}
</style>
