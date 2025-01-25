<template>
  <!-- Prepaid Cards Section -->
  <h style="color: aqua; margin: 0px 10px;" class="heading">Prepaid Cards</h>
  
  <!-- Message when no cards are available -->
  <div style="margin: 10px;">
    <h v-if="all_cards.length === 0" style="color: white">Sorry! No card available</h>
  </div>

  <!-- Display user cards -->
  <div class="users_cards">
    <div v-for="card in all_cards" :key="card.card_no" class="card_container">
      <!-- Card Container -->
      <div class="card">
        <!-- Card Header -->
        <div class="card_head">
          <div class="chip"></div>
          <div style="margin-left: 200px;" class="card_type">Prepaid Card</div>
        </div>
        
        <!-- Card Number -->
        <div class="card-number">{{ card.card_no }}</div>
        
        <!-- Card Details -->
        <div class="card-details">
          <div class="name">{{ card.full_name }}</div>
        </div>
        
        <!-- Card Logo -->
        <div class="logo">VISA</div>
      </div>

      <!-- Card Additional Details -->
      <div class="card_details">
        <div class="card_general_details">
          <div class="card_dates">
            <p>Issued: <span>{{ card.date_issued }}</span></p>
            <p>Expiry: <span>{{ card.expiry_date }}</span></p>
          </div>
          <div class="card_status">
            <p>Status: <span>{{ card.status }}</span></p>
            <p>Balance: <span>{{ card.balance }}</span></p>
          </div>
        </div>
      </div>

      <!-- Uncomment buttons section if needed in the future -->
      <!--
      <div class="card_buttons">
        <button type="button" class="btn btn-success">Block</button>
        <button type="button" class="btn btn-success">Reset PIN</button>
        <button type="button" class="btn btn-success">Replace</button>
        <button type="button" class="btn btn-success">Top Up</button>
      </div>
      -->
    </div>
  </div>

  <!-- Link to apply for a prepaid card -->
  <router-link to="/prepaid_card_application">
    <button style="margin-left: 30px; margin-bottom: 20px;" type="button" class="btn btn-success">
      Apply Prepaid
    </button>
  </router-link>
</template>

<script>
/**
 * Prepaid_Cards Component
 * 
 * Displays a list of prepaid cards for the logged-in user, 
 * fetched from the backend API. Includes features to show card
 * details and manage user interaction.
 */
import apiEndpoints from '@/api/apiEndpoints';

export default {
  name: "Prepaid_Cards",
  
  // Component Data
  data() {
    return {
      all_cards: [], // Stores fetched cards
    };
  },

  // Lifecycle hook - Fetch data when component is mounted
  mounted() {
    this.fetchData();
  },

  // Methods for the component
  methods: {
    /**
     * Fetch user prepaid cards from API.
     * Uses stored access token for authentication.
     */
    async fetchData() {
      try {
        const response = await fetch(apiEndpoints.cardService.getUserPC, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });

        const data = await response.json();
        this.all_cards.push(...data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Styling for the Prepaid_Cards Component */

.users_cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
  padding: 20px;
}

.card_container {
  margin-bottom: 20px;
  margin-right: 25px;
  border: 2px solid transparent;
  border-radius: 8px;
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
  padding-left: 20px;
}

.card_container:hover {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  border-color: aqua;
}

.card {
  width: 350px;
  height: 200px;
  border-radius: 15px;
  background: #750000;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: black;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  position: relative;
  margin-right: 40px;
  margin-top: 20px;
  transition: transform 1s ease, box-shadow 1s ease;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px #750000;
}

.card .chip {
  width: 50px;
  height: 35px;
  border-radius: 5px;
  background: gold;
  position: absolute;
  top: 20px;
  left: 20px;
}

.card_head {
  display: flex;
  justify-content: space-around;
  margin: 0;
  padding: 0;
}

.card-number {
  font-size: 1.4em;
  letter-spacing: 2px;
  margin-top: 60px;
}

.card-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.card-details .name {
  font-size: 1em;
  text-transform: uppercase;
}

.logo {
  position: absolute;
  bottom: 20px;
  right: 20px;
  font-weight: bold;
  font-size: 1.2em;
}

.card_general_details {
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
  margin-bottom: 10px;
}

.card_dates {
  margin-right: 50px;
}

.card_details {
  margin-top: 10px;
}

p {
  color: gold;
  font-size: small;
  font-style: italic;
  margin-top: 5px;
}

span {
  color: aqua;
}
</style>
