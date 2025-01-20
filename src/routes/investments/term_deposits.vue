<template>
    <Nav_Bar></Nav_Bar>
    <h1>Term Deposit</h1>
    <form action="#">
      <div class="form-group">
        <label for="account" class="form-label">Choose Account</label>
        <select
          v-model="formData.account"
          id="account"
          name="account"
          class="form-select"
          style="background-color: rgb(0, 19, 31); color: white; width: 50%;"
        >
          <option selected>Select Account to debit</option>
          <option
            v-for="account in all_accounts"
            :key="account.account_no"
          >{{ account.account_type }} {{ account.currency }}:{{ account.account_no }}</option>
        </select>
      </div>
  
      <div class="form-group">
        <p v-if="balance > 0 && formData.amount !== ''" class="within_limit">
          Balance: {{ balance }}
        </p>
        <p v-else-if="balance < 0 && formData.amount !== ''" class="exceed_limit">
          Balance: {{ balance }}, Sorry! Insufficient Funds
        </p>
        <input
          type="text"
          id="amount"
          name="amount"
          v-model="formData.amount"
          placeholder="Enter Amount"
          @input="check_balance"
        />
      </div>
  
  
      <label for="tenure">Tenure (Month/s)</label>
      <input v-model="formData.tenure" type="number" id="tenure" name="tenure" placeholder="Enter tenure in months" required>
      <div>
        <p class="rate">Rate fixed at {{ this.interestRate }}</p>
      </div>
      <div class="form-group">
        <label for="account" class="form-label">Enter your PIN</label>
        <input
          v-model="formData.password"
          type="password"
          id="password"
          name="password"
          placeholder="PIN"
          style="background-color: rgb(0, 19, 31); border: none; border-bottom: 1px solid aqua; width: 25%;"
        />
      </div>
  
      <button type="button" class="btn btn-success" @click="showConfirmation">
        Book Term Deposit
      </button>
    </form>
    <div class="modal-overlay" v-if="isConfirmationVisible">
        <div class="modal-card">
          <h2 class="modal-title">Confirm Details</h2>
          <p class="modal-content">
            Account Number: <span>{{ formData.account }}</span>
          </p>
          <p class="modal-content">
            Tenure: <span>{{ formData.tenure }} months</span>
          </p>
          <p class="modal-content">
            Amount: <span>{{ formData.amount }}</span>
          </p>
          <p class="modal-content">
            Fixed Rate: <span>{{ this.interestRate }}</span>
          </p>
          <p class="modal-content">
            Potential Interest: <span>{{ potentialInterest }}</span>
          </p>
          <div v-if="!isProcessing" class="modal-buttons">
            <button class="modal-btn confirm" @click="confirmTransfer">Yes</button>
            <button class="modal-btn cancel" @click="cancelTransfer">Cancel</button>
          </div>
          <div>

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
  const url2 = "http://127.0.0.1:8000/post/get_user_transactive_accounts";
  import utils from "../../utils/utils";
  import Nav_Bar from "../../components/navbar.vue";
  
  export default {
    name: "Term_Deposit",
    components: {
      Nav_Bar
    },
    computed: {
        potentialInterest() {
            return (Number(this.formData.amount) * Math.pow(1 + this.interestRate/100, this.formData.tenure));
        }
    },
    data() {
      return {
        formData: {
          amount: "",
          tenure: "",
          account: "",
          password: "",
        },
        all_accounts: [],
        balance: "",
        isConfirmationVisible: false,
        isProcessing: false,
        interestRate: 4.453
      };
    },
  
    mounted() {
      this.fetchData();
    },
  
    methods: {
      findAndReturnSubsequent(str, char) {
        const index = str.indexOf(char);
        return index !== -1 && index < str.length - 1
          ? str.substring(index + 1)
          : ""; // Character not found or it's the last character
      },
  
      check_balance() {
        if (this.formData.account !== "" && this.formData.amount !== "") {
          for (const account of this.all_accounts) {
            if (
              this.findAndReturnSubsequent(this.formData.account, ":") ===
              account.account_no
            ) {
              this.balance = account.account_balance - this.formData.amount;
            }
          }
        }
      },
  
      confirmTransfer() {
        this.bookTermDeposit();
        this.isProcessing = true;
      },
      cancelTransfer() {
        this.isConfirmationVisible = false;
      },
  
      showConfirmation() {
          // Validate before showing confirmation
          if (utils.checkEmptyValues(this.formData)) {
            alert('Please fill in all required fields.');
            return;
          }
          this.isConfirmationVisible = true;
        },


  
      async bookTermDeposit() {
        try {
          if (utils.checkEmptyValues(this.formData)) {
            throw new Error("Empty Fields");
          }
          const requestBody = utils.generateHmacSignature({
            "amount": Number(this.formData.amount),
            "maturity_period": this.formData.tenure,
            "account": this.findAndReturnSubsequent(this.formData.account, ":"),
          });
          const response = await fetch("http://127.0.0.1:8000/post/book_td", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify(requestBody),
          });
          if (!response.ok) {
            throw new Error("Failed to post data");
          }
          setTimeout(() => {
            this.$router.push("/success");
          }, 2000);
        } catch (error) {
          console.error("Error posting data:", error);
          setTimeout(() => {
            this.$router.push("/failed");
          }, 2000);
        }
      },
  
      async fetchData() {
        try {
          const response = await fetch(url2, {
            method: "GET",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          });
          const data = await response.json();
          this.all_accounts.push(...data);
          this.loading = false;
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  h1 {
    color: gold;
    margin-left: 5px;
    margin-top: 80px;
  }
  .within_limit {
    margin-top: 10px;
    color: green;
  }
  .exceed_limit {
    margin-top: 10px;
    color: red;
  }
  label {
    color: antiquewhite;
    margin-left: 10px;
  }
  
  span {
    color: green;
  }
  form {
    margin-left: 10px;
  }
  #tenure {
    width: 25%;
    background-color: black;
    padding: 10px;
      margin: 10px 0;
      border: 1px solid aqua;
      border-radius: 5px;
      color: white;
  }
  .rate {
    color: gold;
    padding: 15px;
  }
  </style>
  