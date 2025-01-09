<template>
  <h style="color: aqua; margin: 0px 10px;" class="heading">Prepaid Cards</h>
  <div style="margin: 10px;"><h v-if="all_cards.length === 0" style="color: white">Sorry! No card available</h></div>
  <div class="users_cards">
    <div v-for="card in all_cards" :key="card" class="card_container">
      <div class="card">
        <div class="card_head">
          <div class="chip"></div>
          <div style="margin-left: 200px;" class="card_type">Prepaid Card</div>
        </div>
        <div class="card-number">{{ card.card_no }}</div>
        <div class="card-details">
          <div class="name">{{ card.full_name }}</div>
        </div>
        <div class="logo">VISA</div>
      </div>
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
      <div class="card_buttons">
        <button type="button" class="btn btn-success">Block</button>
        <button type="button" class="btn btn-success">Reset PIN</button>
        <button type="button" class="btn btn-success">Replace</button>
        <button type="button" class="btn btn-success">Top Up</button>
      </div>
    </div>
  </div>
  <router-link to="/prepaid_card_application"><button style="margin-left: 30px; margin-bottom: 20px;" type="button" class="btn btn-success">Apply Prepaid</button></router-link>
</template>

<script>
const url2 = "http://127.0.0.1:8000/post/get_user_prepaid_cards";

export default {
  name: "Prepaid_Cards",
  data() {
    return {
      all_cards: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch(url2, {
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

.card_buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
  margin-left: 20px;
  margin-bottom: 20px;
}

.btn {
  margin-right: 30px;
}

p {
  color: white;
  font-size: small;
  font-style: italic;
  margin-top: 5px;
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
