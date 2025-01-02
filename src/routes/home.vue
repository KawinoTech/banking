<template>
    <Nav_Bar></Nav_Bar>
    <Exchange_Rate style="margin-top: 80px;"></Exchange_Rate>
    <Hero_Section></Hero_Section>
    
    <div style="background-color: aqua; height: 2px; width: 85%; margin-top: 80px; margin-left: 40px;">.</div>
    <h1 style="color: gold; margin-top: 30px;padding-left: 40px;">Financial Services</h1>
    <Financial_Services></Financial_Services>

    <div style="background-color: aqua; height: 2px; width: 85%; margin-top: 80px; margin-left: 40px;">.</div>
    <h1 style="color: gold; margin-top: 30px;padding-left: 40px;">Assets</h1>
    <Customer_Savings></Customer_Savings>
    <Term_Deposits></Term_Deposits>
    <Current_Accounts></Current_Accounts>

    <div style="background-color: aqua; height: 2px; width: 85%; margin-top: 80px; margin-left: 40px;">.</div>
    <h1 style="color: gold; margin-top: 30px;padding-left: 40px;">Liabilities</h1>
    <Customer_Liability></Customer_Liability>

    <div style="background-color: aqua; height: 2px; width: 85%; margin-top: 80px; margin-left: 40px;">.</div>
    <h1 style="color: gold; margin-top: 30px;padding-left: 40px;">Entertainment</h1>
    <Enter_tainment></Enter_tainment>

    <div style="background-color: aqua; height: 2px; width: 85%; margin-top: 80px; margin-left: 40px;">.</div>
    <h1 style="color: gold; margin-top: 30px;padding-left: 40px;">Transport</h1>
    <Trans_port></Trans_port>

    <div style="background-color: aqua; height: 2px; width: 85%; margin-top: 80px; margin-left: 40px;">.</div>
    <h1 style="color: gold; margin-top: 30px;padding-left: 40px;">Wallets</h1>
    <ThirdP_Wallets></ThirdP_Wallets>
</template>

<script>
import Exchange_Rate from '../components/exchange_r.vue'
import Nav_Bar from '../components/navbar.vue'
import Hero_Section from '../components/hero_section.vue'
import Financial_Services from '../components/financial_services.vue'
import Enter_tainment from '../components/entertainment.vue'
import Trans_port from '../components/transport.vue'
import Customer_Savings from '../components/customer_savings.vue'
import Term_Deposits from '../components/term_deposit.vue'
import Current_Accounts from '../components/current_acs.vue'
import Customer_Liability from '../components/customer_liability.vue'
import ThirdP_Wallets from '../components/thirdp_wallets.vue'
export default {
  name: 'Home_Page',

     data(){
        return {
            loading: true,
        };
     },
     components: {
      Exchange_Rate,
      Nav_Bar,
      Hero_Section,
      Financial_Services,
      Enter_tainment,
      Trans_port,
      Customer_Savings,
      Term_Deposits,
      Current_Accounts,
      Customer_Liability,
      ThirdP_Wallets
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
  .btn {
    display: inline-block;
    padding: 8px 16px;
    background-color: aqua;
    color: rgb(0, 19, 31);
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s ease;
  }
  
  .btn:hover {
    background-color: rgb(0, 19, 31);
    color: aqua;
  }
</style>