<template>
  <Nav_Bar></Nav_Bar>
  <h1>PayBill</h1>
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

    <div class="form-group">
      <label for="account" class="form-label">Paybill Account</label>
      <input
        v-model="formData.account_no"
        type="text"
        id="account_no"
        name="account_no"
        placeholder="Account Number"
      />
    </div>

    <div class="form-group">
      <label for="account" class="form-label">Business No.</label>
      <input
        v-model="formData.beneficiary"
        type="text"
        id="beneficiary"
        name="beneficiary"
        placeholder="Business No."
      />
    </div>

    <div class="form-group">
      <label for="account" class="form-label">Purpose of Payment</label>
      <textarea
        v-model="formData.remarks"
        id="remarks"
        name="remarks"
        placeholder="Remarks"
      ></textarea>
    </div>

    <div class="form-group">
        <label for="account" class="form-label">Choose Network</label>
        <div class="radio-group">
          <label class="radio-option">
            <input type="radio" name="choice" value="option1" />
            Safaricom
          </label>
          <label class="radio-option">
            <input type="radio" name="choice" value="option2" />
            Airtel
          </label>
          <label class="radio-option">
            <input type="radio" name="choice" value="option3" />
            Telkom
          </label>
        </div>
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
      Pay Bill
    </button>
  </form>
  <div class="modal-overlay" v-if="isConfirmationVisible">
      <div class="modal-card">
        <h2 class="modal-title">Confirm Details</h2>
        <p class="modal-content">
          Account Number: <span>{{ formData.account_no }}</span>
        </p>
        <p class="modal-content">
          Paybill Number: <span>{{ formData.beneficiary }}</span>
        </p>
        <p class="modal-content">
          Amount: <span>{{ formData.amount }}</span>
        </p>
        <p class="modal-content">
          Source Account: <span>{{ formData.account }}</span>
        </p>
        <p class="modal-content">
          Description: <span>{{ formData.remarks }}</span>
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
const url2 = "http://127.0.0.1:8000/post/get_user_transactive_accounts";
import utils from "../../utils/utils";
import Nav_Bar from "../../components/navbar.vue";

export default {
  name: "Pay_Bill",
  components: {
    Nav_Bar
  },
  data() {
    return {
      formData: {
        amount: "",
        account_no: "",
        remarks: "",
        beneficiary: "",
        account: "",
        password: "",
      },
      all_accounts: [],
      loading: true,
      balance: "",
      isConfirmationVisible: false,
      isProcessing: false,
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
      this.payBill();
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

    async payBill() {
      try {
        if (utils.checkEmptyValues(this.formData)) {
          throw new Error("Empty Fields");
        }
        const requestBody = utils.generateHmacSignature({
          "amount": Number(this.formData.amount),
          "account": this.findAndReturnSubsequent(this.formData.account, ":"),
          "beneficiary": this.formData.beneficiary,
          "remarks": this.formData.remarks,
          "account_no": this.formData.account_no
        });
        const response = await fetch("http://127.0.0.1:8000/post/paybill", {
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
          this.$router.push("/error");
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
</style>
