<template>
  <!-- Debit Cards Section -->
  <h style="color: aqua; margin: 0 10px;" class="heading">Debit Cards</h>
  
  <!-- Message when no cards are available -->
  <div style="margin: 10px;">
    <h v-if="all_cards.length === 0" style="color: white">Sorry! No card available</h>
  </div>

  <!-- Display user debit cards -->
  <div class="users_cards">
    <div v-for="card in all_cards" :key="card.card_no" class="card_container">
      <!-- Card Container -->
      <div class="card">
        <!-- Card Header -->
        <div class="card_head">
          <div class="chip"></div>
          <div class="card_type">{{ card.card_classification }}</div>
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

      <!-- Additional Details for Card -->
      <div class="card_details">
        <div class="card_general_details">
          <div class="card_dates">
            <p>Date Issued: <span>{{ card.date_issued }}</span></p>
            <p>Expiry Date: <span>{{ card.expiry_date }}</span></p>
          </div>
          <div class="card_status">
            <p>Status: <span>{{ card.status }}</span></p>
            <p>Account: <span>{{ card.account_attached_no }}</span></p>
          </div>
        </div>
      </div>

      <!-- Uncomment this section if needed for button actions -->
      <!--
      <div class="card_buttons">
        <button type="button" class="btn btn-success">Block</button>
        <button type="button" class="btn btn-success">Reset PIN</button>
        <button type="button" class="btn btn-success">Replace</button>
      </div>
      -->
    </div>
  </div>

  <!-- Link to apply for a debit card -->
  <router-link to="/debit_card_application">
    <button style="margin: 30px 10px 20px;" type="button" class="btn btn-success">Apply Debit Card</button>
  </router-link>
</template>

<script>
/**
 * Debit_Cards Component
 *
 * This component displays a list of debit cards for the logged-in user,
 * fetched from a backend API. It includes details such as card number,
 * classification, and account status.
 */
export default {
  name: "Debit_Cards",

  data() {
    return {
      all_cards: [], // Array to store fetched debit cards
    };
  },

  // Fetch card data after the component is mounted
  mounted() {
    this.fetchData();
  },

  methods: {
    /**
     * Fetch Debit Card Data
     * Retrieves the user's debit card information using an API call with the access token.
     */
    async fetchData() {
      try {
        const response = await fetch("http://127.0.0.1:8000/post/get_user_debit_cards", {
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
/* Layout for the entire card collection */
.users_cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
  padding: 15px;
}

/* Individual card container with hover effects */
.card_container {
  margin: 20px 5px 0;
  border: 2px solid transparent;
  border-radius: 8px;
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
}

.card_container:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-color: aqua;
}

/* Card Styling */
.card {
  width: 350px;
  height: 200px;
  border-radius: 15px;
  background: linear-gradient(135deg, #0072ff, #00c6ff);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  position: relative;
  margin: 0px 0px 0;
  transition: transform 0.5s ease, box-shadow 0.5s ease;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgb(118, 216, 255);
}

/* Chip design */
.card .chip {
  width: 50px;
  height: 35px;
  border-radius: 5px;
  background: #e0e0e0;
}

/* Card Head */
.card_head {
  display: flex;
  justify-content: space-around;
  margin: 0;
  padding: 0;
}

/* Card Number */
.card-number {
  font-size: 1.4em;
  letter-spacing: 2px;
  margin-top: 30px;
}

/* Card Details */
.card-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

/* Name section */
.card-details .name {
  font-size: 1em;
  text-transform: uppercase;
}

/* Logo Position */
.logo {
  position: absolute;
  bottom: 20px;
  right: 20px;
  font-weight: bold;
  font-size: 1.2em;
}

/* Card Details Section */
.card_details {
  margin-top: 10px;
}

.card_general_details {
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
  margin: 10px;
}

.card_dates {
  margin-right: 50px;
}

p {
  color: gold;
  font-size: small;
  font-style: italic;
  margin: 5px 0;
}

span {
  color: aqua;
}
</style>
