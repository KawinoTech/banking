<template>
    <h style="color: aqua; margin: 0px 10px 0px 10px;" class="heading">Term Deposits A/Cs</h>
    <div class="container">
    <table class="table table-success table-striped">
  <thead>
    <tr >
      <th scope="col">#</th>
      <th scope="col">Account Number</th>
      <th scope="col">Currency</th>
      <th scope="col">Card Rate</th>
      <th scope="col">Principal</th>
      <th scope="col">Days Remaining</th>
      <th scope="col">#</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
      <td>@mdo</td>
      <td>@mdo</td>
      <td><button type="button" class="btn btn-danger">Liquidate</button></td>
    </tr>
  </tbody>
</table>
</div>
</template>

<script>
export default {
    name: 'Term_Deposits',
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