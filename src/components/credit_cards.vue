<template>
  <h style="color: aqua; margin: 0px 10px 0px 10px;" class="heading">Credit Cards</h>
  <div class="users_cards">
    <div class="card_container">
      <div class="card">
        <div class="chip"></div>
        <div class="card-number">1234 5678 9012 3456</div>
        <div class="card-details">
          <div class="name">John Doe</div>
        </div>
        <div class="logo">VISA</div>
      </div>
      <div class="card_details">
        <div class="card_general_details">
          <div class="card_dates">
          <p>Issued: 26-4-2024</p>
          <p>Expiry: 26-4-2024</p>
        </div>
        <div class="card_status">
          <p>Status: Active</p>
          <p>Limit: Ksh 10,000</p>
        </div>
        </div>
        <p>Balance: Ksh -3,458.45</p>
        <p>Due Date: 26-4-2024</p>
      </div>
    </div>
  </div>
  <div class="card_buttons">
    <button type="button" class="btn btn-success">Block</button>
    <button type="button" class="btn btn-success">Reset PIN</button>
    <button type="button" class="btn btn-success">Repay</button>
    <button type="button" class="btn btn-success">Replace</button>
    <button type="button" class="btn btn-success">Limit Enhancement</button>
  </div>
</template>

<script>
export default {
  name: "Credit_Cards",
};
</script>

<style scoped>
.users_cards {
  display: flex;
  flex-wrap: wrap; /* Allow elements to wrap to the next row */
  justify-content: start;
  padding: 20px;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px gold;
}

.card {
  width: 350px;
  height: 200px;
  border-radius: 15px;
  background: black;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: rgba(255, 217, 0, 0.575);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  position: relative;
  margin-right: 40px;
  margin-top: 20px;
  transition: transform 1s ease, box-shadow 1s ease;
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

.card-details .expiry {
  font-size: 0.9em;
  text-align: right;
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
.card_general_details{
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
}
.card_dates {
  margin-right: 50px;
}
</style>
