<template>
    <div class="container">
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-brands fa-amazon-pay" style="color: aqua;"></i></h5>
                  <router-link to="/amazon_pay"><p  class="btn">Amazon Pay</p></router-link>
                </div>
            </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-brands fa-apple-pay" style="color: aqua;"></i></h5>
                  <router-link to="/apple_pay"><p class="btn">Apple Pay</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-brands fa-google-pay" style="color: aqua;"></i></h5>
                  <router-link to="/google_pay"><p class="btn">Google Pay</p></router-link>
                </div>
              </div>
        </div>
        <div>
            <div class="card">
                <div class="card-content">
                  <h5 class="card-title"><i class="fa-brands fa-paypal" style="color: aqua;"></i></h5>
                  <router-link to="/pay_pal"><p class="btn">PayPal</p></router-link>
                </div>
              </div>
        </div>
    </div>
</template>
<script>
export default {
  name: 'ThirdP_Wallets',

     data(){
        return {
            loading: true,
        };
     },
}
</script>

<style scoped>
.container {
    margin: 20px;
    width: 100%;
    display: flex;
    flex-wrap: wrap; /* Allow elements to wrap to the next row */
    justify-content: space-between;
}
p {
  color: antiquewhite;
}
p:hover {
  color: gold;
}
.card {
    background-color: rgb(0, 19, 31);
    border: 2px solid transparent; /* Set initial border */
    border-radius: 8px;
    overflow: hidden;
    transition: box-shadow 0.3s ease, border-color 0.3s ease; /* Add border-color to transition */
    width: 180px;
    height: 170px;
  }
  
  .card:hover {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    border-color: aqua; /* Change border color on hover */
  }
  
  
  .card-content {
    padding: 20px;
    text-align: center;
  }
  
  .card-title {
    margin-bottom: 20px;
    font-size: 50px;
  }
</style>