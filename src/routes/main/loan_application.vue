<template>
  <Nav_Bar></Nav_Bar>
  <div class="choose_section">
    <button
            id="custom-button"
            class="base-color"
            v-bind:class="modePersonalloan && 'custom-color'"
            @click.prevent="switchPersonalloan">
            Personal Loan
    </button>
    <button
            id="custom-button"
            class="base-color"
            v-bind:class="modeBusinessloan && 'custom-color'"
            @click.prevent="switchBusinesloan">
            Business Loan
    </button>
    <button
            id="custom-button"
            class="base-color"
            v-bind:class="modeMortgage && 'custom-color'"
            @click.prevent="switchMortgage">
            Mortgage Facility
    </button>
  </div>
  <Personal_Loan v-if="modePersonalloan"></Personal_Loan>
  <Business_Loan v-if="modeBusinessloan"></Business_Loan>
  <Mortgage_Facility v-if="modeMortgage"></Mortgage_Facility>
  <Footer></Footer>
</template>


<script>
import Nav_Bar from '../../components/navbar.vue';
import Personal_Loan from '../../components/loans/personal_loan.vue';
import Business_Loan from '../../components/loans/business_loan.vue';
import Mortgage_Facility from '../../components/loans/mortgage.vue';
import Footer from '@/components/others/footer.vue';

export default {
  name: 'New_Loan',
  components: { Nav_Bar,  Personal_Loan, Business_Loan, Mortgage_Facility, Footer},

  data() {
    return {
      modePersonalloan: true,
      modeBusinessloan: false,
      modeMortgage: false
    }
  },

  methods: {
    switchPersonalloan() {
      this.modePersonalloan = true;
      this.modeMortgage = false;
      this.modeBusinessloan = false;
    },
    switchBusinesloan() {
      this.modePersonalloan = false;
      this.modeMortgage = false;
      this.modeBusinessloan = true;
    },
    switchMortgage() {
      this.modePersonalloan = false;
      this.modeMortgage = true;
      this.modeBusinessloan = false;
    }
  }
};
</script>

<style scoped>
.choose_section {
  margin-top: 80px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  padding: 10px;
}

@media (max-width: 850px) {
  #custom-button {
    width: 60%; /* Full width for each item */
    margin-bottom: 10px; /* Space between items */
  }
}

#custom-button {
            font-size: 1rem;
            padding: 10px 20px;
            border: none;
            border-bottom: 2px solid aqua;
            border-right: 2px solid aqua;
            border-radius: 5px;
            text-align: left;
            cursor: pointer;
            transition: background-color 0.3s ease, color 0.3s ease;
            width: 33%;
        }

        #custom-button:hover {
            background-color: aqua;
            color: rgb(0, 19, 31);
        }
        .base-color {
  background-color: rgb(0, 19, 31);
  color: aqua;
}
.custom-color {
  background-color: aqua;
  color: rgb(0, 19, 31);
}

</style>
