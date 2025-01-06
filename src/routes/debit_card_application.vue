<template>
  <Nav_Bar></Nav_Bar>
    <div class="form-container">
    <h1>Debit Card Application</h1>
    <form action="/submit-debit-card-application" method="POST">
      <!-- Personal Information -->
      <label for="full-name">Full Name</label>
      <input type="text" id="full-name" name="full_name" placeholder="Enter your full name" required>

      <label for="dob">Date of Birth</label>
      <input type="date" id="dob" name="date_of_birth" required>

      <label for="email">Email Address</label>
      <input type="email" id="email" name="email" placeholder="Enter your email address" required>

      <label for="phone">Phone Number</label>
      <input type="tel" id="phone" name="phone" placeholder="Enter your phone number" required>

      <!-- Account Details -->
      <label for="account-number">Account Number</label>
      <input type="text" id="account-number" name="account_number" placeholder="Enter your account number" required>

      <label for="account-type">Account Type</label>
      <select id="account-type" name="account_type" required>
        <option value="savings">Savings Account</option>
        <option value="current">Current Account</option>
      </select>

      <!-- Card Preferences -->
      <label for="card-type">Card Type</label>
      <select id="card-type" name="card_type" required>
        <option value="classic">Classic Debit Card</option>
        <option value="platinum">Platinum Debit Card</option>
        <option value="premium">Premium Debit Card</option>
      </select>

      <label for="delivery-option">Delivery Option</label>
      <select id="delivery-option" name="delivery_option" required>
        <option value="branch">Pick up at branch</option>
        <option value="mail">Mail to address</option>
      </select>

      <!-- Terms and Conditions -->
      <label>
        <input type="checkbox" name="terms" required>
        I agree to the terms and conditions.
      </label>

      <!-- Submit Button -->
      <button type="submit">Apply Now</button>
    </form>
  </div>
</template>
<script>
import Nav_Bar from '../components/navbar.vue'
    export default {
        name: "Debit_App",
        components: {
          Nav_Bar
        }
    }
</script>
<style scoped>
    .form-container {
      background-color: rgb(0, 19, 31);
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      width: 50%;
      padding: 20px;
      margin-top: 80px;
    }
    h1 {
  color: gold; margin-left: 5px;
}
    label {
      font-weight: bold;
      margin-bottom: 5px;
      display: block;
      color: white;
    }
    input, select, button {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border: 1px solid aqua;
      border-radius: 5px;
    }
    button {
      background-color: #007bff;
      color: white;
      font-weight: bold;
      cursor: pointer;
      border: none;
    }
    button:hover {
      background-color: #0056b3;
    }
    input, select{
      background-color: rgb(0, 19, 31);
      color: white;
    }
</style>