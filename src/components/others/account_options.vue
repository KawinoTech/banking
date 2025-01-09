<template>
    <div class="container">
        <div class="imag">
            <ImageCarousel :images="carouselImages" />
        </div>
        <div class="descrip">
            <h1>Welcome to the new
            Internet Banking</h1>
            <p>Our internet banking platform lets you access a wide range of 
                services and have your banking needs met without having to physically 
                visit the bank. Transfer money, pay bills, 
                download statements and enjoy being in control of your account.
            </p>
            <div class="accounts">
                <div>
                    <i class="fa-solid fa-piggy-bank"></i><br>
                    <router-link to="/savings_account"><button type="button" class="btn btn-primary">Savings</button></router-link>
                </div>
                <div>
                    <i class="fa-solid fa-person"></i><br>
                    <router-link to="/transactional_account"><button type="button" class="btn btn-success">Personal</button></router-link>
                </div>
                <div>
                    <i class="fa-regular fa-building"></i><br>
                    <router-link to="/corporate_account"><button type="button" class="btn btn-warning">Corporate</button></router-link>
                </div>
                <div>
                    <i class="fa-solid fa-dollar-sign"></i><br>
                    <router-link to="/investment_banking"><button type="button" class="btn btn-info">Investment Banking</button></router-link>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import ImageCarousel from './ImageCarousel.vue';
export default {
    name: 'Accounts_Options',
    components: {
      ImageCarousel,
    },
    data() {
      return {
        carouselImages: [
        require('@/assets/images/hero_image.jpg'), // If in src/assets
        require('@/assets/images/services.jpg'),
        require('@/assets/images/online-payment.avif'),
        ],
      };
    },
  };
</script>
<style scoped>
.container {
    height: 300px;
    width: 100%;
    display: flex;
    justify-content: space-evenly;
    margin-left: 2px;
    margin-right: 2px;
}

h1, p {
    color: gold;
    text-align: start;
}
p {
    color: aqua;
    font-weight: lighter;
}
.descrip {
    margin-left: 30px;
}
.accounts {
    margin-top: 30px;
    display: flex;
    justify-content: space-between;
}
i {
    margin: 20px;
    font-size: 40px;
    color: white;
    color: rgba(255, 217, 0, 0.603);
}

.btn {
    background: gold;
    color: white;
    border: 0;
}
</style>