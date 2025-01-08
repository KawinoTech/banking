<template>
<Nav_Bar></Nav_Bar>
<Exchange_Rate style="margin-top: 80px;"></Exchange_Rate>
<h1>My Cards</h1>
<div><Debit_Cards></Debit_Cards></div>
<div><Credit_Cards></Credit_Cards></div>
<div><Prepaid_Cards></Prepaid_Cards></div>



</template>

<script>
import Nav_Bar from '../components/navbar.vue'
import Exchange_Rate from '../components/exchange_r.vue'
import Debit_Cards from '../components/debit_cards.vue'
import Credit_Cards from '../components/credit_cards.vue'
import Prepaid_Cards from '../components/prepaid_cards.vue'
export default {
    name: "My_Cards",
    components: {
        Nav_Bar,
        Exchange_Rate,
        Credit_Cards,
        Debit_Cards,
        Prepaid_Cards
    }
}
</script>
<style scoped>
h1 {
  color: gold;
  margin-left: 5px;
}

.users_cards {
    display: flex;
    flex-wrap: wrap; /* Allow elements to wrap to the next row */
    justify-content: start;
    padding: 20px;
}
.card {
      width: 350px;
      height: 200px;
      border-radius: 15px;
      background: linear-gradient(135deg, #0072ff, #00c6ff);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      color: white;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 20px;
      position: relative;
      margin-right: 40px;
      margin-top: 20px;
    }

    .card .chip {
      width: 50px;
      height: 35px;
      border-radius: 5px;
      background: #e0e0e0;
      position: absolute;
      top: 20px;
      left: 20px;
    }

    .card-number {
      font-size: 1.4em;
      letter-spacing: 2px;
      margin-top: 60px;
    }

    .card-details {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: auto;
    }

    .card-details .name {
      font-size: 1em;
      text-transform: uppercase;
    }

    .card-details .expiry {
      font-size: 0.9em;
      text-align: right;
    }

    .logo {
      position: absolute;
      bottom: 20px;
      right: 20px;
      font-weight: bold;
      font-size: 1.2em;
    }
</style>