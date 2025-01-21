<template>
    <div class="container">
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-money-bill-transfer" style="color: aqua;"></i></h5>
                  <router-link to="/transfer_funds"><p  class="btn">Transfer Funds</p></router-link>
                </div>
            </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-cart-shopping" style="color: aqua;"></i></h5>
                  <router-link to="/buygoods"><p class="btn">Buy Goods</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-regular fa-credit-card" style="color: aqua;"></i></h5>
                  <router-link to="/my_cards"><p class="btn">My Cards</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-timeline" style="color: aqua;"></i></h5>
                  <router-link to="/transaction_history"><p class="btn">Transaction History</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-piggy-bank" style="color: aqua;"></i></h5>
                  <router-link to="/new_account"><p class="btn">New Account</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-house-signal" style="color: aqua;"></i></h5>
                  <router-link to="/paybill"><p class="btn">Pay Bill</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-regular fa-clock" style="color: aqua;"></i></h5>
                  <router-link to="/appy_term_deposit"><p class="btn">Term Deposit</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-book" style="color: aqua;"></i></h5>
                  <router-link to="/loan_application"><p class="btn">Loan</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-sim-card" style="color: aqua;"></i></h5>
                  <router-link to="/airtime"><p class="btn">Airtime</p></router-link>
                </div>
            </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-money-bill-trend-up" style="color: aqua;"></i></h5>
                  <router-link to="/paybill"><p class="btn">FinMarket</p></router-link>
                </div>
            </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-solid fa-lock" style="color: aqua;"></i></h5>
                  <router-link to="/paybill"><p class="btn">Close Account</p></router-link>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
  name: 'Financial_Services',

     data(){
        return {
            loading: true,
        };
     },
}
</script>

<style scoped>
.container {
    margin: 20px;
    width: 100%;
    display: flex;
    flex-wrap: wrap; /* Allow elements to wrap to the next row */
    justify-content: space-between;
}
p {
  color: antiquewhite;
}
p:hover {
  color: gold;
}
.card {
    background-color: rgb(0, 19, 31);
    border: 2px solid transparent; /* Set initial border */
    border-radius: 8px;
    overflow: hidden;
    transition: box-shadow 0.3s ease, border-color 0.3s ease; /* Add border-color to transition */
    width: 180px;
    height: 170px;
  }
  
  .card:hover {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    border-color: aqua; /* Change border color on hover */
  }
  
  
  .card-content {
    padding: 20px;
    text-align: center;
  }
  
  .card-title {
    margin-bottom: 20px;
    font-size: 50px;
  }
</style>