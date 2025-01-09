<template>
    <h style="color: aqua; margin: 0px 10px 0px 10px;" class="heading">Obligations</h>
    <div class="container">
    <table class="table table-success table-striped">
  <thead>
    <tr >
      <th scope="col">#</th>
      <th scope="col">Account Number</th>
      <th scope="col">Type</th>
      <th scope="col">Principal</th>
      <th scope="col">Accrued Int.</th>
      <th scope="col">Principal Paid</th>
      <th scope="col">Outst. Amount</th>
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
    name: 'Customer_Liability',
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