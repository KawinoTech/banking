<template>
  <h 
    style="color: aqua; margin: 0px 10px 0px 10px;" 
    class="heading">
    Term Deposits A/Cs
  </h>
  <div class="container">
    <table class="table table-success table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Account Number</th>
          <th scope="col">Card Rate</th>
          <th scope="col">Principal</th>
          <th scope="col">Maturity</th>
          <th scope="col">Days remaining</th>
          <th scope="col">#</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(term_deposit, index) in all_term_deposits" :key="index">
          <th scope="row">{{ index + 1 }}</th>
          <td><span>{{ term_deposit.account_no }}</span></td>
          <td><span>{{ term_deposit.rate }}</span></td>
          <td><span>{{ term_deposit.amount }}</span></td>
          <td><span>{{ term_deposit.maturity_date }}</span></td>
          <td><span>{{ term_deposit.days_to_expiry }}</span></td>
          <td>
            <button 
              type="button" 
              class="btn btn-danger" 
              @click="showConfirmation">
              Liquidate
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="modal-overlay" v-if="isConfirmationVisible">
      <div class="modal-card">
        <h2 class="modal-title">Confirm Details</h2>
        <p class="caution">Please note that liquidating before maturity date
          <br>may potentially mean all accrued interest will be lost
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
import utils from "../../utils/utils";
export default {
    name: 'Term_Deposits',
    data() {
      return {
        all_term_deposits : [],
        isConfirmationVisible: false,
        isProcessing: false,
      }
    },
    mounted() {
    this.fetchData();
  },
    methods: {
      async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/post/get_user_term_deposits', {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        const data = await response.json();
        this.all_term_deposits.push(...data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async liquidate(accountNo) {
            try {
              const requestBody = utils.generateHmacSignature({ account_no: accountNo })
                const response = await fetch(`http://127.0.0.1:8000/post/liquidate`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                    body: JSON.stringify(requestBody)
                });

                if (response.ok) {
                  setTimeout(() => {
          this.$router.push("/success");
        }, 2000);
                } else {
                    const errorData = await response.json();
                    alert(`Failed to liquidate: ${errorData.detail || "Unknown error"}`);
                }
            } catch (error) {
                console.error("Error liquidating term deposit:", error);
                alert("An error occurred while liquidating the term deposit. Please try again.");
            }
        },
        showConfirmation() {
      this.isConfirmationVisible = true;
    },
        confirmTransfer() {
          this.isProcessing = true;
          this.liquidate(this.accountNo);
    },
    cancelTransfer() {
      this.isConfirmationVisible = false;
    }
    }
};
</script>

<style scoped>
.heading {
    text-decoration: underline;
}
.container {
    margin: 10px 20px 10px 20px;
}
span {
  font-size: small;
}
.caution {
  color: aqua;
}
</style>