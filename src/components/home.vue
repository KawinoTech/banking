<template>
<div>
    <h1 style="color: aqua; margin: 10px;">My Accounts</h1>
    <User_Accounts></User_Accounts>
    <div class="container px-4 text-center">
        <div class="row gx-5">
          <div class="col">
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-money-bill-transfer" style="color: aqua;"></i></h5>
                  <router-link to="/transfer_funds"><p  class="btn">Transfer Funds</p></router-link>
                </div>
              </div>
          </div>
          <div class="col">
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-cart-shopping" style="color: aqua;"></i></h5>
                  <router-link to="/buygoods"><p class="btn">Buy Goods</p></router-link>
                </div>
              </div>
          </div>
        </div>
      </div>
      <div class="container px-4 text-center">
        <div class="row gx-5">
          <div class="col">
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-regular fa-credit-card" style="color: aqua;"></i></h5>
                  <router-link to="/my_cards"><p class="btn">My Cards</p></router-link>
                </div>
              </div>
          </div>
          <div class="col">
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-timeline" style="color: aqua;"></i></h5>
                  <router-link to="/transaction_history"><p class="btn">Transaction History</p></router-link>
                </div>
              </div>
          </div>
        </div>
      </div>
      <div class="container px-4 text-center">
        <div class="row gx-5">
          <div class="col">
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-piggy-bank" style="color: aqua;"></i></h5>
                  <router-link to="/new_account"><p class="btn">New Account</p></router-link>
                </div>
              </div>
          </div>
          <div class="col">
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-house-signal" style="color: aqua;"></i></h5>
                  <router-link to="/paybill"><p class="btn">Pay Bill</p></router-link>
                </div>
              </div>
          </div>
        </div>
      </div>
</div>
</template>

<script>
import User_Accounts from './user_accounts.vue'
export default {
  name: 'Home_Page',

     data(){
        return {
            loading: true,
        };
     },
     components: {
      User_Accounts,
     },

  methods: {
    async fetchData() {
        try {
            const response = await fetch('');
            const data = await response.json();
            for (let i = 0; i < data.currencies.length; i++)
            {
                this.currencies.push(data.currencies[i]);
            }
            this.loading = false;
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
  }
}
</script>

<style scoped>
.head, .table{
  margin: 20px;
}
.table {
  width: 70%;
}
</style>