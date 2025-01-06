import Buy_goods from '../routes/buygoods.vue'
import Home_Page from '../routes/home.vue'
import Pay_Bill from '../routes/paybill.vue'
import Debit_App from '../routes/debit_card_application.vue'
import Credit_App from '../routes/credit_card_application.vue'
import Prepaid_App from '../routes/prepaid_card_application.vue'
import Savings_Account from '../routes/savings.vue'
import Investment_Banking from '../routes/investment_banking.vue'
import Transactional_Account from '../routes/transactional_account.vue'
import Corporate_Account from '../routes/corporate_banking.vue'
import New_Account from '../routes/new_account.vue'
import Transfer_Funds from '../routes/transfer_funds.vue'
import Transaction_History from '../routes/transaction_history.vue'
import Login_Page from '../routes/login.vue'
import My_Cards from '../routes/mycards.vue'
import Login_Error_pg from '../components/loginerror.vue'
import Error_pg from '../routes/error.vue'
import Success_Pg from '../routes/success.vue'
import Customer_Service from '../routes/customer_service.vue'
import Report_Problem from '../routes/report_problem.vue'
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        name: 'Goods',
        component: Buy_goods,
        path: '/buygoods'
    },
    {
        name: 'Error_pg',
        component: Error_pg,
        path: '/failed'
    },
    {
        name: 'Success_Pg',
        component: Success_Pg,
        path: '/success'
    },
    {
        name: 'Home',
        component: Home_Page,
        path: '/home'
    },
    {
        name: 'Bill',
        component: Pay_Bill,
        path: '/paybill'
    },
    {
        name: 'Transfer',
        component: Transfer_Funds,
        path: '/transfer_funds'
    },
    {
        name: 'NewAcc',
        component: New_Account,
        path: '/new_account'
    },
    {
        name: 'Trans',
        component: Transaction_History,
        path: '/transaction_history'
    },
    {
        name: 'Login_Page',
        component: Login_Page,
        path: '/'
    },
    {
        name: 'My_Cards',
        component: My_Cards,
        path: '/my_cards'
    },
    {
        name: 'Login_Error_pg',
        component: Login_Error_pg,
        path: '/invalid_credentials'
    },
    {
        name: 'Customer_Service',
        component: Customer_Service,
        path: '/customer_service'
    },
    {
        name: 'Report_Problem',
        component: Report_Problem,
        path: '/report_problem'
    },
    {
        name: 'Savings_Account',
        component: Savings_Account,
        path: '/savings_account'
    },
    {
        name: 'Transactional_Account',
        component: Transactional_Account,
        path: '/transactional_account'
    },
    {
        name: 'Corporate_Account',
        component: Corporate_Account,
        path: '/corporate_account'
    },
    {
        name: 'Investment_Banking',
        component: Investment_Banking,
        path: '/investment_banking'
    },
    {
        name: 'Debit_App',
        component: Debit_App,
        path: '/debit_card_application'
    },
    {
        name: 'Credit_App',
        component: Credit_App,
        path: '/credit_card_application'
    },
    {
        name: 'Prepaid_App',
        component: Prepaid_App,
        path: '/prepaid_card_application'
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

export default router;