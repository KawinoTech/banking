<template>
<div class="overlay">
<!-- LOGN IN FORM by Omar Dsoky -->
<form>
   <div class="con">
   <header class="head-form">
      <h2>Log In</h2>
      <p>Login here using your Customer no. and password</p>
   </header>
   <br>
   <div class="field-set">
    
         <span class="input-item">
           <i class="fa fa-user-circle"></i>
         </span>
         <input v-model="formData.customer_no" class="form-input" id="txt-input" type="text" placeholder="@Customer No." required>
     
      <br>
     
      <span class="input-item">
        <i class="fa fa-key"></i>
       </span>
      <input v-model="formData.password_hash" class="form-input" type="password" placeholder="Password" id="pwd"  name="password" required>
     <span>
        <i class="fa fa-eye" aria-hidden="true"  type="button" id="eye"></i>
     </span>
     
     
      <br>
      <button class="log-in" @click.prevent="login"> Log In </button>
   </div>
  
   <div class="other">

      <button class="btn submits frgt-pass">Forgot Password</button>

   </div>
  </div>
</form>
</div>
</template>
<script>
import apiEndpoints from "../../api/apiEndpoints"

export default ({
    name: "Login_Page",
    data() {
        return {
            formData: {
            customer_no: '',
            password_hash: ''
        },
        }
        
    },

methods: {

    async login() {
      try {
        const response = await fetch(apiEndpoints.auth.login, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData),
        });
                          if (!response.ok) {
                  throw new Error('Failed to Login in');
        }
        const data = await response.json();
        const { access_token, expires_in } = data
        // Storing the access token in localStorage
        localStorage.setItem("accessToken", access_token);
        localStorage.setItem("expiresAt", new Date(expires_in).getTime());
        // Redirect to another page after successful login
        this.$router.push('/home');
      } catch (error) {
        console.error('Error:', error);
                setTimeout(() => {
          this.$router.push('/invalid_credentials');
        }, 2000);
      }
    }
  }
}
)

</script>
<style scoped>


form {
    width: 450px;
    min-height: 500px;
    height: auto;
    border-radius: 5px;
    margin: 2% auto;
    box-shadow: 0 9px 50px aqua;
    padding: 2%;
    background-image: linear-gradient(-225deg, #E3FDF5 50%, #048479 50%);
}
/* form Container */
form .con {
    display: -webkit-flex;
    display: flex;
  
    -webkit-justify-content: space-around;
    justify-content: space-around;
  
    -webkit-flex-wrap: wrap;
    flex-wrap: wrap;
  
      margin: 0 auto;
}

/* the header form form */
header {
    margin: 2% auto 10% auto;
    text-align: center;
}
/* Login title form form */
header h2 {
    font-size: 250%;
    font-family: 'Playfair Display', serif;
    color: #3e403f;
}
/*  A welcome message or an explanation of the login form */
header p {letter-spacing: 0.05em;}



/* //////////////////////////////////////////// */
/* //////////////////////////////////////////// */


.input-item {
    background: white;
    color: #333;
    padding: 14.5px 0px 15px 9px;
    border-radius: 5px 0px 0px 5px;
}



/* Show/hide password Font Icon */
#eye {
    background: #fff;
    color: #333;
  
    margin: 5.9px 0 0 0;
    margin-left: -20px;
    padding: 15px 9px 19px 0px;
    border-radius: 0px 5px 5px 0px;
  
    float: right;
    position: relative;
    right: 1%;
    top: -.2%;
    z-index: 5;
    
    cursor: pointer;
}
/* inputs form  */
input[class="form-input"]{
    width: 240px;
    height: 50px;
    background: white;
  
    margin-top: 2%;
    padding: 15px;
    
    font-size: 16px;
    font-family: 'Abel', sans-serif;
    color: #5E6472;
  
    outline: none;
    border: none;
  
    border-radius: 0px 5px 5px 0px;
    transition: 0.2s linear;
    
}
input[id="txt-input"] {width: 250px;}
/* focus  */
input:focus {
    transform: translateX(-2px);
    border-radius: 5px;
}

/* //////////////////////////////////////////// */
/* //////////////////////////////////////////// */

/* input[type="text"] {min-width: 250px;} */
/* buttons  */
button {
    display: inline-block;
    color: #252537;
  
    width: 280px;
    height: 50px;
  
    padding: 0 20px;
    background: #fff;
    border-radius: 5px;
    
    outline: none;
    border: none;
  
    cursor: pointer;
    text-align: center;
    transition: all 0.2s linear;
    
    margin: 7% auto;
    letter-spacing: 0.05em;
}
/* Submits */
.submits {
    width: 48%;
    display: inline-block;
    float: left;
    margin-left: 2%;
}

/*       Forgot Password button FAF3DD  */
.frgt-pass {background: transparent;}

/*     Sign Up button  */
.sign-up {background: #B8F2E6;}


/* buttons hover */
button:hover {
    transform: translatey(3px);
    box-shadow: none;
}

/* buttons hover Animation */
button:hover {
    animation: ani9 0.4s ease-in-out infinite alternate;
}
@keyframes ani9 {
    0% {
        transform: translateY(3px);
    }
    100% {
        transform: translateY(5px);
    }
}

</style>
