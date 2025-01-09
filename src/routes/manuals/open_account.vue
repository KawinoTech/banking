<template>
<Nav_Bar></Nav_Bar>
<main>
  <h2 style="font-size: 40px;">Opening a Transactional Account</h2>
  <p>
    Opening an account with us is a simple process, but certain details need to be provided for verification and to ensure compliance with legal and financial regulations. 
    This manual will guide you step-by-step to prepare the required information and explain why each detail is necessary.
  </p>

  <h2>Step 1: Gather Required Information</h2>
  <p>Below is the list of information you'll need to successfully open an account:</p>
  <ul>
    <li><b class="highlight">Account Name:</b> This is the official name associated with your account. Ensure it includes at least <span class="highlight">three names</span>, separated by spaces, for example, "John Michael Doe". Avoid abbreviations.</li>
    <li><b class="highlight">Email Address:</b> Use a valid and accessible email address in the format <span class="highlight">example@example.com</span>. We will use this to send account-related information.</li>
    <li><b class="highlight">Telephone:</b> Provide a phone number starting with your <span class="highlight">country code</span> (e.g., +254712345678 for Kenya).</li>
    <li>
      <b class="highlight">National ID Number:</b> Your government-issued ID number is necessary for verification through the official IPRS API. Make sure it matches your official records.
    </li>
    <li>
      <b class="highlight">KRA PIN:</b> This tax identification number will be verified using the <span class="highlight">I-Tax API</span>. It helps ensure compliance with tax laws and checks your status with CRB for financial credibility.
    </li>
    <li>
      <b class="highlight">Next of Kin:</b> A trusted person to contact in case of emergencies. This name should be different from your account name, ensuring clarity in our records.
    </li>
    <li>
      <b class="highlight">Relationship:</b> Clearly specify the relationship with the next of kin. Accepted values are "brother," "sister," or "relative".
    </li>
    <li>
      <b>Type of Account:</b> Choose the account type that best fits your needs:
      <ul>
        <li><b class="highlight">Pay as You Go:</b> Personal accounts for individuals managing day-to-day finances.</li>
        <li><b class="highlight">SME Banking:</b> Tailored for small and medium-sized businesses for operational transactions.</li>
        <li><b class="highlight">Vue Vantage:</b> Designed for clubs, associations, or non-profits for collaborative financial activities.</li>
        <li><b class="highlight">Forex Plus:</b> A foreign currency account for transactions and financial derivatives.</li>
      </ul>
    </li>
    <li>
      <b class="highlight">Nationality:</b> Your country of origin to align your account with legal regulations and reporting frameworks.
    </li>
  </ul>

  <h2>Step 2: Understand Each Input Requirement</h2>
  <p>Let’s break down each input with more details:</p>
  <ol>
    <li><span class="highlight">Account Name:</span> Include your full official name as it appears in your government-issued identification documents. Nicknames or informal abbreviations may delay account approval.</li>
    <li><span class="highlight">Email Address:</span> Ensure this address is functional. You will receive OTPs, verification emails, and statements at this email.</li>
    <li><span class="highlight">Telephone:</span> A valid phone number allows us to contact you and secure your account through 2-factor authentication.</li>
    <li><span class="highlight">National ID:</span> Your ID number will be cross-referenced with government systems to confirm your identity.</li>
    <li><span class="highlight">KRA PIN:</span> This is crucial for individuals in Kenya. Compliance with I-Tax ensures smooth transactions and access to financial services.</li>
    <li><span class="highlight">Next of Kin:</span> Provide a responsible and reachable contact person, especially in cases where consent or emergency action may be needed.</li>
    <li><span class="highlight">Type of Account:</span> Select the account type most appropriate for your financial needs and usage.</li>
  </ol>

  <h2>Step 3: Ready to Open Your Account?</h2>
  <p>
    Once you’ve gathered all the information outlined above, you’re ready to open your account. The next steps may require providing these details on our secure portal or visiting your nearest branch for identity verification. Remember to double-check all the inputs for accuracy.
  </p>

  <h2>Need More Help?</h2>
  <p>
    If you have any issues or questions, feel free to contact our customer service team via email at <span class="highlight">support@examplebank.com</span> or call us at <span class="highlight">+123-456-7890</span>. We’re here to assist you every step of the way.
  </p>
</main>
</template>
<script>
import Nav_Bar from '../../components/navbar.vue'
    export default {
        name: 'Manual_Open_Account',
        emits: ['close'],
        data() {
            return {
                data1: "Hello"
            }
        },
        components: {
          Nav_Bar
}
    }
</script>
<style lang="css" scoped>
main {
    max-width: 800px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h1, h2 {
    color: gold;
}

h1 {
    font-size: 30px;
}

h2 {
    font-size: 24px;
    margin-top: 80px;
}

p, ul {
    margin-bottom: 15px;
}

ul {
    padding-left: 20px;
}

li {
    margin-bottom: 10px;
}

.highlight {
    font-weight: bold;
    color: #007BFF;
}

footer {
    text-align: center;
    font-size: 14px;
    color: #777;
    margin-top: 20px;
}
p, span, li{
  color: white;
}
.highlight {
  color: aqua;
}
</style>