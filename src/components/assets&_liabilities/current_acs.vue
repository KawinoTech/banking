<template>
    <h style="color: aqua; margin: 0px 10px 0px 10px;" class="heading">Current A/Cs</h>
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
  </tbody>
</table>
</div>
</template>

<script>
export default {
    name: 'Current_Accounts',
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