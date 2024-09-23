<template>
            <div class="head">
            <p style="color: rgb(196, 186, 186);">Transaction History</p>
        </div>
    <div class="transaction-details" v-for="trans in paginatedItems" :key="trans.id">
        <p><span class="label">Account Type:</span>{{trans.account_type}}</p>
        <p><span class="label">Currency:</span> {{trans.curr}}</p>
        <p><span class="label">Amount:</span> <span class="amount">{{trans.amount}}</span></p>
        <p><span class="label">Beneficiary:</span> {{trans.beneficiary}}</p>
        <p><span class="label">Transaction Time:</span> {{trans.transaction_time}}</p>
        <p><span class="label">Reference No:</span>{{trans.ref_no}}</p>
        <p><span class="label">Transaction Type:</span>Deposit</p>
  </div>
      <button type="button" class="btn btn-success" @click="prevPage" :disabled="currentPage === 1">Previous</button>
    <span>Page {{ currentPage }} of {{ totalPages }}</span>
    <button type="button" class="btn btn-success" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
</template>
<script>
import json from '../assets/transaction_history.json'
export default {
    name: "Transaction_History",

     data(){
        return {
            loading: true,
            all_transactions: [],
            currentPage: 1,
            itemsPerPage: 2
        }
    },
    mounted() {
        this.fetchJson();
    },
     methods: {
        async fetchData() {
            try {
                const response = await fetch('./transaction_history.json');
                const data = await response.json();
                for (let i = 0; i < data.transactions.length; i++)
                {
                    this.all_transactions.push(data.transactions[i]);
                }
                this.loading = false;
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        fetchJson() {
        try {
        for (let i = 0; i < json.transactions.length; i++)
        {
            this.all_transactions.push(json.transactions[i]);
        }
        this.loading = false;
    } 
    catch (error) 
    {
    console.error('Error fetching data:', error);
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
    }
            
     },
       computed: {
    totalPages() {
      return Math.ceil(this.all_transactions.length / this.itemsPerPage);
    },
    paginatedItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.all_transactions.slice(startIndex, endIndex);
    }
  }
}
</script>
<style scoped>
.head {
    color: rgb(196, 186, 186);
    font-size: 30px;
    margin: 20px;
}
</style>