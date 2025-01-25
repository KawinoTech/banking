const API_BASE_URL = "http://127.0.0.1:8000";

const apiEndpoints = {
  auth: {
    login: `${API_BASE_URL}/post/login`,
  },
  transactions: {
    c2bTransfer: `${API_BASE_URL}/post/transfer`,
    buyGoods: `${API_BASE_URL}/post/buygoods`,
    payBill: `${API_BASE_URL}/post/paybill`,
    airtime: `${API_BASE_URL}/post/airtime`,
    topUpWallet: `${API_BASE_URL}/post/topup_wallet`,
    allCurrentUserTransactions: `${API_BASE_URL}/post/all_user_transactions`,
  },
  accounts: {
    getTransactiveaccounts: `${API_BASE_URL}/post/get_user_transactive_accounts`,
    closeAccount: (accountNo) => `${API_BASE_URL}/post/close_account/${accountNo}`,
    openPersonalAccount: `${API_BASE_URL}/post/open_personal_account`,
    openForeignCurrency: `${API_BASE_URL}/post/open_foreign_currency_account`,
    openBusinessAccount: `${API_BASE_URL}/post/open_corporate_account`,
    getCurrentaccounts: `${API_BASE_URL}/post/get_user_current_accounts`,
    getSavingsaccounts: `${API_BASE_URL}/post/get_user_savings_accounts`,
  },
  loans: {
    getTransactiveloans: `${API_BASE_URL}/post/get_user_transactive_loans`,
    getUserloans: `${API_BASE_URL}/post/get_user_loans`,
    applyPersonalLoan: `${API_BASE_URL}/post/apply_personal_loan`,
    applyBusinessLoan: `${API_BASE_URL}/post/apply_business_loan`,
    applyMortgage: `${API_BASE_URL}/post/apply_business_loan`,
  },
  termDeposits: {
    bookTD: `${API_BASE_URL}/post/book_td`,
    getUserTds: `${API_BASE_URL}/post/get_user_term_deposits`,
    liquidate: `${API_BASE_URL}/post/liquidate`,
  },
  helpDesk: {
    requestHelp: `${API_BASE_URL}/post/request_help`,
    report: `${API_BASE_URL}/post/report_problem`,
  },
  cardService: {
    applyCreditCard: `${API_BASE_URL}/post/credit_card_application`,
    applyDebitCard: `${API_BASE_URL}/post/debit_card_application`,
    applyPrepaidCard: `${API_BASE_URL}/post/prepaid_card_application`,
    getUserCC: `${API_BASE_URL}/post/get_user_credit_cards`,
    getUserDC: `${API_BASE_URL}/post/get_user_debit_cards`,
    getUserPC: `${API_BASE_URL}/post/get_user_prepaid_cards`,
  }
};

export default apiEndpoints;
