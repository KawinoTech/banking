<template>
  <Nav_Bar></Nav_Bar>
  <div class="choose_section">
    <button
            id="custom-button"
            class="base-color"
            v-bind:class="modePersonalAcc && 'custom-color'"
            @click.prevent="switchPersonalAcc">
            Personal Account
    </button>
    <button
            id="custom-button"
            class="base-color"
            v-bind:class="modeCorporateAcc && 'custom-color'"
            @click.prevent="switchCorporateAcc">
            Business Account
    </button>
    <button
            id="custom-button"
            class="base-color"
            v-bind:class="modeFCAcc && 'custom-color'"
            @click.prevent="switchFCAcc">
            Foreign Currency Account
    </button>
  </div>
  <Personal_Account v-if="modePersonalAcc"></Personal_Account>
  <Corporate_Account v-if="modeCorporateAcc"></Corporate_Account>
  <Foreign_Currency_Account v-if="modeFCAcc"></Foreign_Currency_Account>
</template>


<script>
import Nav_Bar from '../../components/navbar.vue';
import Personal_Account from '../../components/account_opening/personal_acc.vue';
import Corporate_Account from '../../components/account_opening/corporate_acc.vue';
import Foreign_Currency_Account from '../../components/account_opening/foreign_currency.vue';


export default {
  name: 'New_Account',
  components: { Nav_Bar,  Personal_Account, Corporate_Account, Foreign_Currency_Account},

  data() {
    return {
      modePersonalAcc: true,
      modeCorporateAcc: false,
      modeFCAcc: false
    }
  },

  methods: {
    switchPersonalAcc() {
      this.modePersonalAcc = true;
      this.modeFCAcc = false;
      this.modeCorporateAcc = false;
    },
    switchCorporateAcc() {
      this.modePersonalAcc = false;
      this.modeFCAcc = false;
      this.modeCorporateAcc = true;
    },
    switchFCAcc() {
      this.modePersonalAcc = false;
      this.modeFCAcc = true;
      this.modeCorporateAcc = false;
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
