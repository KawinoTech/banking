<template>
<div class="head">
    <p style="color: rgb(196, 186, 186); text-decoration: underline;">Check Out our Products</p>
</div>
<div class="container text-center">
  <div class="row align-items-center">
    <div class="col">
      <i class="fa-solid fa-lock" style="color: red;"></i>
      <p>Savings Account</p>
      <p>Interest-bearing deposit account</p>
      <p>Opening balance - Kes 1000.</p>
      <p>Zero monthly fees.</p>
    </div>
    <div class="col">
      <i class="fa-solid fa-wallet" style="color: green;"></i>
      <p>Pay As You Go</p>
      <p>avails you an account that allows you 
        to access your funds on a regular basis through various 
        instruments like a cheque book and a debit card</p>
    </div>
    <div class="col">
      <i class="fa-solid fa-dollar-sign" style="color: yellow;"></i>
      <p>Forex Plus</p>
      <p>Do you have businesses abroad? Make payments overseas? Manage your money with a Foreign 
        Currency Current Account. Operate your account in major 
        foreign currencies such as the Euro, Dollar and British Pound, in addition to the Kenyan shilling.</p>
    </div>
  </div>
</div>
<div class="container text-center">
  <div class="row align-items-center">
    <div class="col">
      <i class="fa-solid fa-business-time" style="color: orange;"></i>
        <p>SME Banking</p>
        <p>Explore the small business solutions and choose the account 
          that's right for your business. NBK offers a wide range of products to meet SME needs</p>
    </div>
    <div class="col">
      <i class="fa-solid fa-building" style="color: blue;"></i>
      <p>Corporate Banking</p>
      <p>provide financial services like cash management, payment processing, 
        credit products, and hedging strategies to large corporations</p>
    </div>
  </div>
</div>
</template>
<script>
export default {
    name: "Image_Slider"
}
</script>
<style scoped>
i{
    font-size: 30px;
}
p {
    color: aqua;
    font-size: 15px;
}
.head {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>