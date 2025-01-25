<template>
  <!-- Heading Section -->
  <h class="heading" style="color: aqua; margin: 0px 10px 0px 10px;">Current A/Cs</h>

  <!-- Accounts Table -->
  <div v-if="all_accounts.length > 0" class="container">
    <table class="table table-success table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Account Number</th>
          <th scope="col">Currency</th>
          <th scope="col">Amount</th>
          <th scope="col">Equivalent Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(account, index) in all_accounts" :key="index">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ account.account_no }}</td>
          <td>{{ account.currency }}</td>
          <td>{{ account.account_balance }}</td>
          <td>{{ calculateEquivalentAmount(account) }}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- No Data Message -->
  <div v-else class="no-data">
    <p>No current accounts available.</p>
  </div>
</template>

<script>
import apiEndpoints from "@/api/apiEndpoints";

export default {
  name: "CurrentAccounts",
  data() {
    return {
      all_accounts: [], // Holds the fetched accounts
    };
  },
  mounted() {
    this.fetchData(); // Fetch data when the component is mounted
  },
  methods: {
    /**
     * Fetch data from the backend API.
     */
    async fetchData() {
      try {
        const response = await fetch(apiEndpoints.accounts.getCurrentaccounts, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.statusText}`);
        }

        const data = await response.json();
        this.all_accounts = data; // Populate the accounts array with fetched data
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },

    /**
     * Calculate the equivalent amount for a given account.
     * For now, this method simply returns the account balance. Adjust as needed.
     * @param {Object} account - The account object.
     * @returns {Number} The equivalent amount.
     */
    calculateEquivalentAmount(account) {
      return account.account_balance; // Placeholder for actual conversion logic
    },
  },
};
</script>

<style scoped>
/* Style for the main heading */
.heading {
  text-decoration: underline;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

/* Styling for the container holding the table */
.container {
  margin: 20px auto;
  padding: 10px;
  width: 90%;
}

/* Table cell styles */
span {
  font-size: 0.9rem;
  font-weight: 500;
}

/* Styling for the no data message */
.no-data {
  text-align: center;
  font-size: 1.2rem;
  color: gray;
  margin-top: 20px;
}
</style>
