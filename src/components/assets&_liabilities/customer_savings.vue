<template>
    <h style="color: aqua; margin: 0px 10px 0px 10px;" class="heading">Savings A/Cs</h>
    <div class="container">
    <table class="table table-success table-striped">
  <thead>
    <tr >
      <th scope="col">#</th>
      <th scope="col">Account Number</th>
      <th scope="col">Currency</th>
      <th scope="col">Amount</th>
      <th scope="col">Equivalent amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Jacob</td>
      <td>Thornton</td>
      <td>@fat</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td colspan="2">Larry the Bird</td>
      <td>@twitter</td>
    </tr>
  </tbody>
</table>
</div>
</template>

<script>
export default {
    name: 'Customer_Savings',
};
</script>

<style scoped>
.heading {
    text-decoration: underline;
}
.container {
    margin: 10px 20px 10px 20px;
}
</style>