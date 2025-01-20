<template>
  <div class="terms-container">
    <h1>Bank Account Opening Terms and Conditions</h1>

    <h2>1. General Information</h2>
    <p>By opening a bank account with Vue Bank, you agree to the following terms and conditions. Please read them carefully before proceeding.</p>

    <h2>2. Eligibility</h2>
    <ul>
      <li>You must be at least 18 years old to open a bank account.</li>
      <li>You must provide valid identification documents as required by the bank.</li>
      <li>You must not have any unresolved debts with the bank or other financial institutions.</li>
    </ul>

    <h2>3. Account Maintenance</h2>
    <ul>
      <li>You are responsible for maintaining the confidentiality of your account details, including your username, password, and PIN.</li>
      <li>The bank may charge monthly maintenance fees depending on the type of account you open.</li>
      <li>Minimum balance requirements may apply, depending on the account type.</li>
    </ul>

    <h2>4. Fees and Charges</h2>
    <p>Vue Bank may charge fees for certain services related to your account, including but not limited to:</p>
    <ul>
      <li>ATM withdrawals outside the bank's network.</li>
      <li>Wire transfers and foreign exchange transactions.</li>
      <li>Overdraft protection services.</li>
    </ul>

    <h2>5. Modification of Terms</h2>
    <p>Vue Bank reserves the right to modify these terms and conditions at any time. Any changes will be communicated to you through the contact information provided in your account details.</p>

    <h2>6. Account Closure</h2>
    <p>You may request to close your account at any time, subject to the following conditions:</p>
    <ul>
      <li>The account must not have any pending transactions or unresolved fees.</li>
      <li>Any outstanding balance must be cleared before the account can be closed.</li>
    </ul>

    <div class="footer">
      <p>Thank you for choosing Vue Bank. We look forward to serving you.</p>
    </div>
  </div>
  </template>
  
  <script>
  export default {
    name: "Terms_Conditions",
    data() {
      return {
        showTerms: false,
        isAgreed: false,
      };
    },
    methods: {
      proceed() {
        this.$router.push('/new_account')
      },
    },
  };
  </script>
  
  <style scoped>
    .terms-container {
      max-width: 800px;
      margin: 40px auto;
      padding: 20px;
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 0 10px rgb(0, 19, 31);
    }

    h1 {
      text-align: center;
      color: #007bff;
    }

    h2 {
      color: #0056b3;
    }

    p {
      font-size: 16px;
      margin: 10px 0;
    }

    ul {
      list-style-type: disc;
      padding-left: 20px;
    }

    li {
      margin: 8px 0;
      font-size: 16px;
    }

    .footer {
      margin-top: 30px;
      text-align: center;
      font-size: 14px;
      color: #888;
    }
  </style>
  