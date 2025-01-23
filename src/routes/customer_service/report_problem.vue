<template>
    <Nav_Bar></Nav_Bar>
    <div class="report-problem-section">
    <h2>Report a Problem</h2>
    <p>If you encounter any issues or wish to report anonymously, please use the form below. Alternatively, you can reach out to us through the following emergency lines:</p>
    <ul class="emergency-contacts">
        <li><i class="fa-solid fa-phone"></i><strong>Hotline 1:</strong> +1-800-123-4567</li>
        <li><i class="fa-solid fa-phone"></i><strong>Hotline 2:</strong> +1-800-765-4321</li>
        <li><i class="fa-regular fa-envelope"></i><strong>Email:</strong> emergency@company.com</li>
        <li><i class="fa-brands fa-whatsapp"></i><strong>WhatsApp:</strong> +1-900-123-4567</li>
    </ul>
    <form class="report-form">
        <div class="form-group">
            <label for="message">Message:</label>
            <p v-if="formData.text === ''" class="empty">Fill in the required space*</p>
            <textarea v-model="formData.text" type="text" id="text" name="text" placeholder="Describe the issue..." required></textarea>
        </div>
        <button class="btn" type="submit" @click.prevent="showConfirmation">Report</button>
    </form>
</div>
<div class="modal-overlay" v-if="isConfirmationVisible">
      <div class="modal-card">
        <h2 class="modal-title">Confirm Details</h2>
        <p class="modal-content">
          Dear Customer, our team will swiftly get <br>back to you immediately to give feedback
        </p>
        <div v-if="!isProcessing" class="modal-buttons">
          <button class="modal-btn confirm" @click="confirm">Yes</button>
          <button class="modal-btn cancel" @click="cancel">Cancel</button>
        </div>
        <div v-if="isProcessing">
          <p class="wait">
            Processing<i class="fa-regular wait fa-clock fa-spin"></i>
          </p>
        </div>
      </div>
    </div>
</template>
<script>
import Nav_Bar from '../../components/navbar.vue'
import utils from '../../utils/utils'
export default {
  name: 'Report_Problem',

     data(){
        return {
            submitted: false,
            isConfirmationVisible: false,
            isProcessing: false,
            formData: {
            text: ''
        }
        };
     },
     components: {
        Nav_Bar
     },
     methods: {
     async reportProblem() {
     this.submitted = true;
     try{
          const response = await fetch('http://127.0.0.1:8000/post/report_problem',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
            },
              body: JSON.stringify(
                {
                "text": this.formData.text,}
              )
          });
          if (!response.ok) {
                        throw new Error('Failed to post data');
              }
          setTimeout(() => {
                this.$router.push('/success');
          }, 2000);
        }
        catch (error) {
        console.error('Error posting data:', error);
        setTimeout(() => {
                this.$router.push('/failed');
          }, 1000);
        this.submitted = false;
      }
      },
      showConfirmation() {
      if (utils.checkEmptyValues(this.formData)) {
        alert("Please fill in the required fields.");
        return;
      }
      this.isConfirmationVisible = true;
    },
    confirm() {
      this.reportProblem();
      this.isProcessing = true;
    },
    cancel() {
      this.isConfirmationVisible = false;
    },
    }
};

</script>
<style scoped>
.report-problem-section {
    max-width: 800px;
    margin-top: 80px;
    padding: 20px;
}

.report-problem-section h2 {
    text-align: start;
    color: gold;
}

.report-problem-section p {
    font-size: 16px;
    color: aqua;
    text-align: start;
    margin-bottom: 20px;
}

.emergency-contacts {
    list-style-type: none;
    padding: 0;
    margin: 0 0 20px 0;
    text-align: start;
}

.emergency-contacts li {
    font-size: 16px;
    color: white;
    margin: 5px 0;
}

.report-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    font-size: 14px;
    color: gold;
    margin-bottom: 5px;
}

.form-group input,
.form-group textarea {
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.form-group input:focus,
.form-group textarea:focus {
    border-color: #007BFF;
    outline: none;
}

textarea {
    resize: vertical;
    min-height: 100px;
}

button {
  margin-top: 15px;
  padding: 10px 15px;
  font-size: 16px;
  color: #fff;
  background-color: #28a745;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: rgba(255, 0, 0, 0.514);
  color: white;
}

i {
    margin-right: 20px;
    color: green;
    font-size: larger;
}
.empty {
  font-family: 'Times New Roman', Times, serif;
  font-style: italic;
  font-weight: lighter;
  color: red;
}
.btn {
  width: 100px;
  background: red;
}
</style>