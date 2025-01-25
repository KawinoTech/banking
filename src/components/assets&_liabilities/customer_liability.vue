<template>
  <!-- Heading Section -->
  <h class="heading" style="color: aqua; margin: 0px 10px 0px 10px;">Obligations</h>

  <!-- Obligations Table -->
  <div v-if="all_accounts.length > 0" class="container">
    <table class="table table-success table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Account Number</th>
          <th scope="col">Type</th>
          <th scope="col">Principal</th>
          <th scope="col">Accrued Int.</th>
          <th scope="col">Principal Paid</th>
          <th scope="col">Disposable</th>
          <th scope="col">Outstanding Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(account, index) in all_accounts" :key="index">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ account.account_no }}</td>
          <td>{{ account.account_type }}</td>
          <td>{{ account.amount }}</td>
          <td>{{ account.accrued_interest }}</td>
          <td>{{ account.principal_paid }}</td>
          <td>{{ account.disposable_amount }}</td>
          <td>{{ account.outstanding_amount }}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- No Data Message -->
  <div v-else class="no-data">
    <p>No obligations found for the user.</p>
  </div>
</template>

<script>
import apiEndpoints from "@/api/apiEndpoints";

export default {
  name: "CustomerLiability",
  data() {
    return {
      all_accounts: [], // Holds the list of user obligations
    };
  },
  mounted() {
    this.fetchData(); // Fetch data when the component is mounted
  },
  methods: {
    /**
     * Fetch user obligations from the backend API.
     */
    async fetchData() {
      try {
        const response = await fetch(apiEndpoints.loans.getUserloans, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.statusText}`);
        }

        const data = await response.json();
        this.all_accounts = data; // Populate obligations list with fetched data
      } catch (error) {
        console.error("Error fetching data:", error);
      }
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
