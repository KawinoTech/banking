<template>
    <Nav_Bar></Nav_Bar>
    <div class="form-container">
    <h1>Prepaid Card Application</h1>
    <form action="/submit-prepaid-card-application" method="POST">
      <!-- Personal Information -->
      <label for="full-name">Full Name</label>
      <input type="text" id="full-name" name="full_name" placeholder="Enter your full name" required>

      <label for="email">Email Address</label>
      <input type="email" id="email" name="email" placeholder="Enter your email address" required>

      <label for="phone">Phone Number</label>
      <input type="tel" id="phone" name="phone" placeholder="Enter your phone number" required>

      <label for="dob">Date of Birth</label>
      <input type="date" id="dob" name="date_of_birth" required>

      <!-- Card Details -->
      <label for="card-amount">Preloaded Amount (USD)</label>
      <input type="number" id="card-amount" name="card_amount" placeholder="Enter the initial amount to load" required>

      <label for="currency">Preferred Currency</label>
      <select id="currency" name="currency" required>
        <option value="">Select Currency</option>
        <option value="usd">USD - United States Dollar</option>
        <option value="eur">EUR - Euro</option>
        <option value="gbp">GBP - British Pound</option>
        <option value="inr">INR - Indian Rupee</option>
        <option value="aud">AUD - Australian Dollar</option>
      </select>

      <label for="usage">Intended Usage</label>
      <input type="text" id="usage" name="usage" placeholder="E.g., Online shopping, travel (optional)" class="optional">

      <!-- Terms and Conditions -->
      <label class="terms">
        <input type="checkbox" name="terms" required>
        I agree to the terms and conditions.
      </label>

      <!-- Submit Button -->
      <button type="submit">Apply for Prepaid Card</button>
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
      padding: 25px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
      width: 50%;
      margin-top: 80px;
    }

    h1 {
  color: gold; margin-left: 5px;
}

    label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
      color: white;
    }

    input, select, button {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border: 1px solid aqua;
      border-radius: 5px;
      box-sizing: border-box;
    }

    button {
      background-color: #28a745;
      color: white;
      border: none;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    button:hover {
      background-color: #218838;
    }

    .terms {
      font-size: 0.9em;
      color: #555;
      display: flex;
      align-items: center;
    }

    .terms input {
      margin-right: 10px;
    }

    .optional {
      font-size: 0.85em;
      color: #999;
    }
    input, select{
      background-color: rgb(0, 19, 31);
      color: white;
    }
</style>