<template>
    <Nav_Bar></Nav_Bar>
      <div class="form-container">
    <h1>Credit Card Application</h1>
    <form action="/submit-credit-card-application" method="POST">
      <!-- Personal Information -->
      <label for="full-name">Full Name</label>
      <input type="text" id="full-name" name="full_name" placeholder="Enter your full name" required>

      <label for="dob">Date of Birth</label>
      <input type="date" id="dob" name="date_of_birth" required>

      <label for="email">Email Address</label>
      <input type="email" id="email" name="email" placeholder="Enter your email address" required>

      <label for="phone">Phone Number</label>
      <input type="tel" id="phone" name="phone" placeholder="Enter your phone number" required>

      <!-- Employment Details -->
      <label for="employment-status">Employment Status</label>
      <select id="employment-status" name="employment_status" required>
        <option value="employed">Employed</option>
        <option value="self-employed">Self-Employed</option>
        <option value="student">Student</option>
        <option value="unemployed">Unemployed</option>
      </select>

      <label for="annual-income">Annual Income (USD)</label>
      <input type="number" id="annual-income" name="annual_income" placeholder="Enter your annual income" required>

      <!-- Card Preferences -->
      <label for="card-type">Preferred Card Type</label>
      <select id="card-type" name="card_type" required>
        <option value="standard">Standard Credit Card</option>
        <option value="gold">Gold Credit Card</option>
        <option value="platinum">Platinum Credit Card</option>
        <option value="business">Business Credit Card</option>
      </select>

      <!-- Address -->
      <label for="address">Address</label>
      <input type="text" id="address" name="address" placeholder="Enter your residential address" required>

      <!-- Terms and Conditions -->
      <label class="terms">
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
    }

    button {
      background-color: #007bff;
      color: white;
      border: none;
      font-weight: bold;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #0056b3;
    }

    .terms {
      font-size: 0.9em;
      color: #555555;
      display: flex;
      align-items: center;
    }

    .terms input {
      margin-right: 10px;
    }
    input, select{
      background-color: rgb(0, 19, 31);
      color: white;
    }
</style>