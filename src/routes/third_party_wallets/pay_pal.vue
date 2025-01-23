<template>
    <Nav_Bar></Nav_Bar>
    <h1>Top up</h1>
    <div class="main_container">
        <div class="form-container">
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
                    >
                        {{ account.account_type }} {{ account.currency }}:{{ account.account_no }}
                    </option>
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
                    <input
                    v-model="formData.beneficiary"
                    type="text"
                    id="beneficiary"
                    name="beneficiary"
                    placeholder="PayPal Account"
                    />
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
                    Top Up
                </button>
            </form>
        </div>
        <div class="icon-container">
            <i class="fa-brands fa-paypal" style="color: aqua;"></i>
        </div>
    </div>
    <div class="modal-overlay" v-if="isConfirmationVisible">
            <div class="modal-card">
                <h2 class="modal-title">Confirm Details</h2>
                <p class="modal-content">
                Account Number: <span>{{ formData.account }}</span>
                </p>
                <p class="modal-content">
                Beneficiary: <span>{{ formData.beneficiary }}</span>
                </p>
                <p class="modal-content">
                Amount: <span>{{ formData.amount }}</span>
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
    name: "Pay_Pal",
    components: {
      Nav_Bar,
    },
    data() {
      return {
        formData: {
          amount: "",
          beneficiary: "",
          account: "",
          service_provider: "Pay Pal",
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
          : "";
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
        if (utils.checkEmptyValues(this.formData)) {
          alert("Please fill in all required fields.");
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
            amount: Number(this.formData.amount),
            beneficiary: this.formData.beneficiary,
            account: this.findAndReturnSubsequent(this.formData.account, ":"),
          });
          const response = await fetch("http://127.0.0.1:8000/post/topup_wallet", {
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
  i {
    color: aqua;
    font-size: 500px;
    margin: 0;
    padding: 0;
  }
  .main_container {
  display: flex;
  justify-content: start;
  align-items: flex-start; /* Aligns items at the top */
  flex-wrap: wrap; /* Enables wrapping of flex items */
}

.form-container {
  width: 60%;
  min-width: 300px; /* Ensures the form has a minimum width */
}

.icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30%;
  min-width: 150px; /* Minimum width for smaller screens */
}

/* Media query to adjust layout for smaller screens */
@media (max-width: 768px) {
  .main_container {
    flex-direction: column; /* Stacks items vertically */
    align-items: center; /* Centers them horizontally */
  }

  .form-container,
  .icon-container {
    width: 100%; /* Make both containers take full width */
    margin-bottom: 20px; /* Add some spacing between them */
  }

 i {
    font-size: 300px; /* Reduce icon size for smaller screens */
  }
}

</style>
  