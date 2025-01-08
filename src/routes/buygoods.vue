<template>
  <div>
    <Nav_Bar></Nav_Bar>
    <form action="#">
      <h1>Buy Goods</h1>
      <div class="form-group">
        <label for="account" class="form-label">Select Account to debit</label>
        <select
          v-model="formData.account"
          id="account"
          name="account"
          class="form-select"
          style="background-color: rgb(0, 19, 31); color: white; width: 50%;"
        >
          <option v-for="account in all_accounts" :key="account">
            {{ account.account_type }} {{ account.currency }}:{{ account.account_no }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <input
          v-model="formData.beneficiary"
          type="text"
          id="beneficiary"
          name="beneficiary"
          placeholder="Store Number"
        />
      </div>
      <div class="form-group">
        <p
          v-if="balance > 0 && formData.amount != ''"
          class="within_limit"
        >
          Balance: {{ balance }}
        </p>
        <div
          class="overdraft"
          v-else-if="balance < 0 && formData.amount != ''"
        >
          <p class="exceed_limit">
            Balance: {{ balance }}, Sorry! Insufficient Funds
          </p>
          <button type="button" class="btn btn-success">Request Overdraft</button>
        </div>
        <input
          v-model="formData.amount"
          type="text"
          id="amount"
          name="amount"
          placeholder="Enter Amount"
          @input="check_balance"
        />
      </div>
      <div class="form-group">
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
        <input
          v-model="formData.password"
          type="password"
          id="password"
          name="password"
          placeholder="PIN"
          style="
            background-color: rgb(0, 19, 31);
            border: none;
            border-bottom: 1px solid aqua;
            width: 25%;
          "
        />
      </div>
      <button type="button" class="btn btn-success" @click="showConfirmation">
        Buy Goods
      </button>
    </form>
    <div class="modal-overlay" v-if="isConfirmationVisible">
      <div class="modal-card">
        <h2 class="modal-title">Confirm Details</h2>
        <p class="modal-content">
          Store: <span>{{ formData.store_no }}</span>
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
  </div>
</template>

<script>
import utils from "../utils/utils";
import Nav_Bar from "../components/navbar.vue";
const url2 = "http://127.0.0.1:8000/post/get_user_accounts";

export default {
  name: "Buy_goods",
  data() {
    return {
      formData: {
        amount: "",
        remarks: "",
        beneficiary: "",
        account: "",
        password: "",
      },
      all_accounts: [],
      isConfirmationVisible: false,
      isProcessing: false,
    };
  },
  components: {
    Nav_Bar,
  },
  mounted() {
    this.fetchData();
  },
  methods: {
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
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    findAndReturnSubsequent(str, char) {
      const index = str.indexOf(char);
      return index !== -1 && index < str.length - 1
        ? str.substring(index + 1)
        : "";
    },
    showConfirmation() {
      if (utils.checkEmptyValues(this.formData)) {
        alert("Please fill in all required fields.");
        return;
      }
      this.isConfirmationVisible = true;
    },
    confirmTransfer() {
      this.buyGoods();
      this.isProcessing = true;
    },
    cancelTransfer() {
      this.isConfirmationVisible = false;
    },
    check_balance() {
      if (this.formData.account && this.formData.amount) {
        const account = this.all_accounts.find(
          (acc) =>
            this.findAndReturnSubsequent(this.formData.account, ":") ===
            acc.account_no
        );
        if (account) {
          this.balance = account.account_balance - this.formData.amount;
        }
      }
    },
    async buyGoods() {
      try {
        if (utils.checkEmptyValues(this.formData)) {
          throw new Error("Empty Fields");
        }
        const requestBody = utils.generateHmacSignature({
          amount: Number(this.formData.amount),
          account: this.findAndReturnSubsequent(this.formData.account, ":"),
          remarks: this.formData.remarks,
          beneficiary: this.formData.beneficiary,
        });
        const response = await fetch("http://127.0.0.1:8000/post/buygoods", {
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
  },
};
</script>

<style scoped>
h1 {
  color: gold;
  margin-left: 5px;
}
form {
  margin-left: 10px;
  margin-top: 80px;
}
label {
  color: white;
}
span {
  color: green;
}
</style>
