import Buy_goods from '../routes/buygoods.vue'
import Home_Page from '../routes/home.vue'
import Pay_Bill from '../routes/paybill.vue'
import New_Account from '../routes/new_account.vue'
import Transfer_Funds from '../routes/transfer_funds.vue'
import Transaction_History from '../routes/transaction_history.vue'
import Login_Page from '../routes/login.vue'
import My_Cards from '../routes/mycards.vue'
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