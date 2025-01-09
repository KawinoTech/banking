<template>
    <Nav_Bar></Nav_Bar>
    <div class="background-container">
  </div>
    <section id="customer-care">
  <div class="contact-info">
    <h2>Contact Customer Care</h2>
    <p1>We’re here to help! You can reach us through the following ways:</p1>
    <ul>
      <li><p>Email:</p> <a href="mailto:support@example.com">support@example.com</a></li>
      <li><p>Phone:</p> <a href="tel:+1234567890">+1 (234) 567-890</a></li>
      <li><p>Live Chat:</p> <a href="#">Start a live chat</a></li>
    </ul>
  </div>
  <div class="message-form">
    <h2>Send Us a Message</h2>
    <form action="/submit-message" method="post">

      <label for="message">Message</label>
      <p v-if="formData.text === ''" class="empty">Fill in the required space*</p>
      <textarea v-model="formData.text" type="text" id="text" name="text" placeholder="Write your message here" required></textarea>

      <button v-if="!submitted" type="submit" @click.prevent="helpDesk">Send Message</button>
      <p v-else>Please wait while we process you request ..<i class="fa-solid fa-hourglass-start fa-spin-pulse"></i></p>
    </form>
  </div>
</section>
</template>
<script>
import Nav_Bar from '../../components/navbar.vue'
import check from '../../utils/utils'
export default {
  name: 'Customer_Service',

     data(){
        return {
            submitted: false,
            formData: {
            text: ''
        },
        error_message: {

        }
        };
     },
     components: {
        Nav_Bar
     },
     methods: {
     async helpDesk() {
     this.submitted = true;
     try{
          if (check.checkEmptyValues(this.formData)){
          throw new Error('Empty Fields');
          }
          const response = await fetch('http://127.0.0.1:8000/post/request_help',
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
          }, 3000);
        }
        catch (error) {
        console.error('Error posting data:', error);
        setTimeout(() => {
                this.$router.push('/failed');
          }, 1000);
        this.submitted = false;
      }
      }
    }
};

</script>
<style scoped>
    .background-container {
      background-image: url('../../assets/images/support.jpg'); /* Replace with your image path */
      background-size: cover; /* Scales image to cover the entire area */
      background-repeat: no-repeat; /* Prevents the image from repeating */
      background-position: center; /* Center aligns the image */
      position: relative;
      height: 100vh;}
#customer-care {
  padding: 20px;
  position: absolute;
  top: 0;
  border-radius: 8px;
  max-width: 600px;
  margin-top: 80px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.contact-info {
  margin-bottom: 20px;
}

.contact-info h2 {
  text-align: start;
  color: gold;
}

.contact-info ul {
  list-style: none;
  padding: 0;
}

.contact-info li {
  margin: 10px 0;
}

.contact-info a {
  color: white;
  text-decoration: none;
}

.contact-info a:hover {
  text-decoration: underline;
}

.message-form h2 {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-size: 24px;
  color: white;
  margin-bottom: 10px;
}

.message-form form {
  display: flex;
  flex-direction: column;
}

.message-form label {
  margin-top: 10px;
  font-weight: bold;
  color: gold;
}

.message-form input,
.message-form textarea {
  margin-top: 5px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  outline: none;
}

.message-form textarea {
  resize: vertical;
  min-height: 100px;
}

.message-form button {
  margin-top: 15px;
  padding: 10px 15px;
  font-size: 16px;
  color: #fff;
  background-color: gold;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 150px;
}

.message-form button:hover {
  background-color: #218838;
}
p {
    color: aqua;
    display: inline;
}

i {
  font-size: large;
  color: green;
  margin-left: 20px;
}
.empty {
  font-family: 'Times New Roman', Times, serif;
  font-style: italic;
  font-weight: bolder;
  color: red;
  padding: 0;
}
p1 {
    font-size: 16px;
    color: aqua;
    text-align: start;
    margin-bottom: 20px;
}
</style>