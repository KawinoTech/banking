<template>
  <Nav_Bar></Nav_Bar>

  <!-- Transaction History Header -->
  <div class="head">
    <p style="color: gold;">Transaction History</p>
  </div>

  <!-- Transaction Table -->
  <table class="table table-success table-striped">
    <thead>
      <tr>
        <th scope="row">#</th>
        <th scope="col">Account</th>
        <th scope="col">Amount</th>
        <th scope="col">Ref_No</th>
        <th scope="col">Beneficiary</th>
        <th scope="col">Type</th>
        <th scope="col">Datetime</th>
        <th scope="col">Action</th>
      </tr>
    </thead>
    <tbody>
      <!-- Render Transactions with Pagination -->
      <tr v-for="(trans, index) in paginatedItems" :key="trans.id">
        <th scope="row">{{ index + 1 + (currentPage - 1) * itemsPerPage }}</th>
        <td><span>{{ trans.account }}</span></td>
        <td><span>KES: {{ trans.amount }}</span></td>
        <td><span>{{ trans.ref_no }}</span></td>
        <td><span>{{ trans.beneficiary }}</span></td>
        <td><span>{{ trans.transaction_type }}</span></td>
        <td><span>{{ trans.date_posted }}</span></td>
        <td>
          <button
            type="button"
            class="btn btn-danger"
            @click="generateReceipt(trans)"
          >
            Download Receipt
          </button>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- Pagination -->
  <div class="pagination">
    <button
      type="button"
      class="btn btn-success"
      @click="prevPage"
      :disabled="currentPage === 1"
    >
      Previous
    </button>
    <span>Page {{ currentPage }} of {{ totalPages }}</span>
    <button
      type="button"
      class="btn btn-success"
      @click="nextPage"
      :disabled="currentPage === totalPages"
    >
      Next
    </button>
  </div>
</template>

<script>
import Nav_Bar from "../../components/navbar.vue";
import jsPDF from "jspdf"; // Import jsPDF library

export default {
  name: "Transaction_History",
  components: { Nav_Bar },

  data() {
    return {
      loading: true,
      all_transactions: [], // Stores all user transactions
      currentPage: 1, // Tracks the current pagination page
      itemsPerPage: 9, // Number of items per page
    };
  },

  mounted() {
    this.fetchData();
  },

  methods: {
    /**
     * Fetches transaction data from the server.
     */
    async fetchData() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/post/all_user_transactions",
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const data = await response.json();
        this.all_transactions.push(...data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },

    /**
     * Moves to the next page of the transaction table.
     */
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    /**
     * Moves to the previous page of the transaction table.
     */
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },

    /**
     * Generates a PDF receipt for a transaction and downloads it.
     * 
     * @param {Object} transaction - The transaction object.
     */
     generateReceipt(transaction) {
  const doc = new jsPDF(); // Create a new jsPDF instance

  // Set background color
  doc.setFillColor(255, 255, 255);  // white background
  doc.rect(0, 0, 210, 297, 'F');   // page size is A4 (210x297 mm)

  // Title
  doc.setFontSize(20);
  doc.setTextColor(0, 0, 0); // Set text color to black
  doc.text("Transaction Receipt", 20, 30); // Centered at x = 20 and y = 30
  
  // Drawing a horizontal line
  doc.setLineWidth(0.5);
  doc.line(10, 35, 200, 35); // Starting from x=10, y=35 to x=200, y=35
  
  // Main content section with stylized data
  doc.setFontSize(12);
  doc.setTextColor(50, 50, 50); // Light grey color for data text
  
  // Account Information Section
  doc.text(`Account: ${transaction.account}`, 20, 50);
  doc.text(`Amount: KES ${transaction.amount}`, 20, 60);
  doc.text(`Ref_No: ${transaction.ref_no}`, 20, 70);
  doc.text(`Beneficiary: ${transaction.beneficiary}`, 20, 80);
  doc.text(`Transaction Type: ${transaction.transaction_type}`, 20, 90);
  doc.text(`Date/Time: ${transaction.date_posted}`, 20, 100);
  
  // Add a vertical line to divide sections (Optional)
  doc.setLineWidth(0.5);
  doc.line(100, 35, 100, 105); // dividing line from y=35 to y=105
  
  // Footer Section
  doc.setFontSize(10);
  doc.setTextColor(100, 100, 100); // Set footer text color
  doc.text("Thank you for using our service.", 20, 240); // Footer text
  
  // Optional: Add logos or branding (example using an image logo)
  // doc.addImage('data:image/png;base64,...', 'PNG', 150, 250, 50, 20); // add image to footer

  // Save the PDF and prompt the user to download
  doc.save(`Receipt_${transaction.ref_no}.pdf`);
}

  },

  computed: {
    /**
     * Computes the total number of pages for pagination.
     */
    totalPages() {
      return Math.ceil(this.all_transactions.length / this.itemsPerPage);
    },

    /**
     * Extracts the items for the current page.
     * 
     * @returns {Array} Paginated transactions.
     */
    paginatedItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.all_transactions.slice(startIndex, endIndex);
    },
  },
};
</script>

<style scoped>
/* Style for the transaction history header */
.head {
  color: gold;
  font-size: 30px;
  margin: 20px;
  margin-top: 80px;
}

/* Style for the pagination section */
.pagination {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

/* Small styling for table rows */
span {
  font-size: small;
}
</style>

