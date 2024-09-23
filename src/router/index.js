import Buy_goods from '../components/buygoods.vue'
import Home_Page from '../components/home.vue'
import Pay_Bill from '../components/paybill.vue'
import New_Account from '../components/new_account.vue'
import Transfer_Funds from '../components/transfer_funds.vue'
import Transaction_History from '../components/transaction_history.vue'
import Success_Pg from '../components/success.vue'
import Error_Pg from '../components/error.vue'
import Login_Page from '../components/login.vue'
import My_Cards from '../components/mycards.vue'
import Login_Error_pg from '../components/loginerror.vue'
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        name: 'Goods',
        component: Buy_goods,
        path: '/buygoods'
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
        name: 'Success_Pg',
        component: Success_Pg,
        path: '/success'
    },
    {
        name: 'Error_Pg',
        component: Error_Pg,
        path: '/error'
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
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

export default router;