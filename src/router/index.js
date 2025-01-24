import Buy_goods from '../routes/transacting/buygoods.vue'
import Pay_Bill from '../routes/transacting/paybill.vue'
import Air_Time from '../routes/transacting/airtime.vue'
import Transfer_Funds from '../routes/transacting/transfer_funds.vue'
import Debit_App from '../routes/card_applications/debit_card_application.vue'
import Credit_App from '../routes/card_applications/credit_card_application.vue'
import Prepaid_App from '../routes/card_applications/prepaid_card_application.vue'
import Amazon_Pay from '../routes/third_party_wallets/amazon_pay.vue'
import Apple_Pay from '../routes/third_party_wallets/apple_pay.vue'
import Google_Pay from '../routes/third_party_wallets/google_pay.vue'
import Pay_Pal from '../routes/third_party_wallets/pay_pal.vue'
import Savings_Account from '../routes/account_products/savings.vue'
import Investment_Banking from '../routes/account_products/investment_banking.vue'
import Transactional_Account from '../routes/account_products/transactional_account.vue'
import Corporate_Account from '../routes/account_products/corporate_banking.vue'
import Customer_Service from '../routes/customer_service/customer_service.vue'
import Report_Problem from '../routes/customer_service/report_problem.vue'
import Home_Page from '../routes/main/home.vue'
import Financial_Markets from '../routes/main/financial_markets.vue'
import My_Cards from '../routes/main/mycards.vue'
import New_Account from '../routes/main/new_account.vue'
import Transaction_History from '../routes/main/transaction_history.vue'
import New_Loan from '../routes/main/loan_application.vue'
import Account_Closure from '../routes/main/account_closure.vue'
import Login_Error_pg from '../routes/error_pages/loginerror.vue'
import Error_pg from '../routes/error_pages/error.vue'
import Not_Found from '../routes/error_pages/404_notfound.vue'
import Login_Page from '../routes/main/login.vue'
import Manual_Open_Account from '../routes/manuals/open_account.vue'
import Success_Pg from '../routes/success.vue'
import Term_Deposit from '../routes/investments/term_deposits.vue'
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        name: 'Goods',
        component: Buy_goods,
        path: '/buygoods'
    },
    {
        name: 'Amazon_Pay',
        component: Amazon_Pay,
        path: '/amazon_pay'
    },
    {
        name: 'Apple_Pay',
        component: Apple_Pay,
        path: '/apple_pay'
    },
    {
        name: 'Google_Pay',
        component: Google_Pay,
        path: '/google_pay'
    },
    {
        name: 'Pay_Pal',
        component: Pay_Pal,
        path: '/pay_pal'
    },
    {
        name: 'Account_Closure',
        component: Account_Closure,
        path: '/account_closure'
    },
    {
        name: 'Financial_Markets',
        component: Financial_Markets,
        path: '/financial_markets'
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
        name: 'Air_Time',
        component: Air_Time,
        path: '/airtime'
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
        alias: '/login',
        path: '/'
    },
    {
        name: 'My_Cards',
        component: My_Cards,
        path: '/my_cards',
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
    },
    {
        name: 'Manual_Open_Account',
        component: Manual_Open_Account,
        path: '/instructions_on_opening_transactional_account'
    },
    {
        name: 'Term_Deposit',
        component: Term_Deposit,
        path: '/appy_term_deposit'
    },
    {
        name: 'New_Loan',
        component: New_Loan,
        path: '/loan_application'
    },
    {
        /*Routes any unmatching route*/
        path: '/:pathMatch(.*)*', 
        name: 'Not_Found',
        component: Not_Found
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

export default router;