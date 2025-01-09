<template>
  <Nav_Bar></Nav_Bar>

  <div class="head">
    <p style="color: gold;">Transaction History</p>
  </div>

  <table class="table table-success table-striped">
    <thead>
      <tr>
        <th scope="row">#</th>
        <th scope="col">Account</th>
        <th scope="col">Amount</th>
        <th scope="col">Beneficiary</th>
        <th scope="col">Datetime</th>
        <th scope="col"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="trans in paginatedItems" :key="trans.id">
        <th scope="row"></th>
        <td>{{ trans.account }}</td>
        <td>KES: {{ trans.amount }}</td>
        <td>{{ trans.beneficiary }}</td>
        <td>{{ trans.date_posted }}</td>
        <td>
          <button type="button" class="btn btn-danger">Download Receipt</button>
        </td>
      </tr>
    </tbody>
  </table>

  <div class="pagination">
    <button type="button" class="btn btn-success" @click="prevPage" :disabled="currentPage === 1">
      Previous
    </button>
    <span>Page {{ currentPage }} of {{ totalPages }}</span>
    <button type="button" class="btn btn-success" @click="nextPage" :disabled="currentPage === totalPages">
      Next
    </button>
  </div>
</template>

<script>
import Nav_Bar from '../../components/navbar.vue';

export default {
  name: "Transaction_History",
  components: {
    Nav_Bar,
  },
  data() {
    return {
      loading: true,
      all_transactions: [],
      currentPage: 1,
      itemsPerPage: 5,
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/post/all_user_transactions', {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        const data = await response.json();
        this.all_transactions.push(...data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
  },
  computed: {
    totalPages() {
      return Math.ceil(this.all_transactions.length / this.itemsPerPage);
    },
    paginatedItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.all_transactions.slice(startIndex, endIndex);
    },
  },
};
</script>

<style scoped>
.head {
  color: gold;
  font-size: 30px;
  margin: 20px;
  margin-top: 80px;
}

.pagination {
  margin: 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
