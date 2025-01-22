<template>
    <h style="color: aqua; margin: 0px 10px 0px 10px;" class="heading">Obligations</h>
    <div class="container">
    <table class="table table-success table-striped">
  <thead>
    <tr >
      <th scope="col">#</th>
      <th scope="col">Account Number</th>
      <th scope="col">Type</th>
      <th scope="col">Principal</th>
      <th scope="col">Accrued Int.</th>
      <th scope="col">Principal Paid</th>
      <th scope="col">Outst. Amount</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(account, index) in all_accounts" :key="index">
      <th scope="row">{{ index }}</th>
      <td><span>{{ account.account_no}}</span></td>
      <td><span>{{ account.loan_type }}</span></td>
      <td><span>{{ account.amount }}</span></td>
      <td><span>{{ account.accrued_interest }}</span></td>
      <td><span>{{ account.principal_paid }}</span></td>
      <td><span>{{ account.outstanding_amount }}</span></td>
    </tr>
  </tbody>
</table>
</div>
</template>

<script>
export default {
    name: 'Customer_Liability',
    data() {
      return {
        all_accounts : [],
      }
    },
    mounted() {
    this.fetchData();
  },
    methods: {
      async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/post/get_user_loans', {
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
  font-size: smaller;
}
</style>