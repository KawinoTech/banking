<template>
  <!-- Heading Section -->
  <h class="heading" style="color: aqua; margin: 0px 10px 0px 10px;">Term Deposits A/Cs</h>

  <!-- Term Deposits Table -->
  <div class="container" v-if="all_term_deposits.length > 0">
    <table class="table table-success table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Account Number</th>
          <th scope="col">Card Rate</th>
          <th scope="col">Principal</th>
          <th scope="col">Maturity</th>
          <th scope="col">Days Remaining</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(term_deposit, index) in all_term_deposits" :key="index">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ term_deposit.account_no }}</td>
          <td>{{ term_deposit.rate }}</td>
          <td>{{ term_deposit.amount }}</td>
          <td>{{ term_deposit.maturity_date }}</td>
          <td>{{ term_deposit.days_to_expiry }}</td>
          <td>
            <button 
              type="button" 
              class="btn btn-danger" 
              @click="showConfirmation(term_deposit.account_no)">
              Liquidate
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- No Data Message -->
  <div v-else class="no-data">
    <p>No term deposit accounts found.</p>
  </div>

  <!-- Confirmation Modal -->
  <div class="modal-overlay" v-if="isConfirmationVisible">
    <div class="modal-card">
      <h2 class="modal-title">Confirm Liquidation</h2>
      <p class="caution">
        Please note that liquidating before the maturity date may result in a loss of accrued interest.
      </p>
      <div v-if="!isProcessing" class="modal-buttons">
        <button class="modal-btn confirm" @click="confirmTransfer">Yes</button>
        <button class="modal-btn cancel" @click="cancelTransfer">Cancel</button>
      </div>
      <div v-else>
        <p class="wait">
          Processing<i class="fa-regular fa-clock fa-spin wait"></i>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import apiEndpoints from "@/api/apiEndpoints";
import utils from "../../utils/utils";

export default {
  name: "TermDeposits",
  data() {
    return {
      all_term_deposits: [], // List of all term deposit accounts
      isConfirmationVisible: false, // Controls the visibility of the confirmation modal
      isProcessing: false, // Indicates if the liquidation process is in progress
      accountNum: "", // Stores the account number for liquidation
    };
  },
  mounted() {
    this.fetchData(); // Fetch term deposit data when the component is mounted
  },
  methods: {
    /**
     * Fetch term deposit accounts from the API.
     */
    async fetchData() {
      try {
        const response = await fetch(apiEndpoints.termDeposits.getUserTds, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        const data = await response.json();
        this.all_term_deposits = data;
      } catch (error) {
        console.error("Error fetching term deposit accounts:", error);
      }
    },

    /**
     * Liquidate the selected term deposit account.
     * @param {String} accountNo - Account number to be liquidated
     */
    async liquidate(accountNo) {
      try {
        const requestBody = utils.generateHmacSignature({ account_no: accountNo });
        const response = await fetch(apiEndpoints.termDeposits.liquidate, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          setTimeout(() => {
            this.$router.push("/success");
          }, 2000);
        } else {
          const errorData = await response.json();
          this.$router.push("/failed");
          console.error(`Failed to liquidate: ${errorData.detail || "Unknown error"}`);
        }
      } catch (error) {
        console.error("Error liquidating term deposit:", error);
        this.$router.push("/failed");
      }
    },

    /**
     * Show the confirmation modal for liquidation.
     * @param {String} accountNo - Account number to be liquidated
     */
    showConfirmation(accountNo) {
      this.isConfirmationVisible = true;
      this.accountNum = accountNo;
    },

    /**
     * Confirm and process the liquidation of the account.
     */
    confirmTransfer() {
      this.isProcessing = true;
      this.liquidate(this.accountNum);
    },

    /**
     * Cancel the liquidation process and close the modal.
     */
    cancelTransfer() {
      this.isConfirmationVisible = false;
    },
  },
};
</script>

<style scoped>
/* Heading styles */
.heading {
  text-decoration: underline;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

/* Table container styles */
.container {
  margin: 20px auto;
  padding: 10px;
  width: 90%;
}

/* Text styling inside table */
span {
  font-size: 0.9rem;
  font-weight: 500;
}

/* No data message styling */
.no-data {
  text-align: center;
  font-size: 1.2rem;
  color: gray;
  margin-top: 20px;
}

/* Modal styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  text-align: center;
}

.modal-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 15px;
}

.caution {
  color: red;
  margin-bottom: 20px;
}

.modal-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 15px;
}

.modal-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.modal-btn.confirm {
  background: green;
  color: white;
}

.modal-btn.cancel {
  background: red;
  color: white;
}

.wait {
  color: gray;
  font-size: 1rem;
}
</style>
