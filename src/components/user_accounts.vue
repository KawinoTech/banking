 <template>
        <div class="dropdown-center">
  <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
    Check Accounts
  </button>
  <ul class="dropdown-menu">
    <li>
    <div class="dropdown-item" href="#">
        <div class="transaction-details" v-for="acc in all_accounts" :key="acc">
        <p><span class="label">Account Type:</span>{{acc.account_type}}</p>
        <p><span class="label">Currency:</span> {{acc.currency}}</p>
        <p><span class="label">Account Balance:</span> <span class="amount">{{acc.account_balance}}</span></p>
        </div>
    </div>
    </li>
  </ul>
  </div>
</template>

<script>
const url2 = 'https://sys-audit.tech/post/get_user_accounts'

export default {
  name: 'User_Accounts',

     data(){
        return {
            loading: true,
            all_accounts: []
        };
     },

    mounted() {
        this.fetchData();
    },

  methods: {

async fetchData() { 
try {
const response = await fetch(url2,
  {method: 'GET',
                                                  headers: {
                                                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                                                  }
                                              }
);
const data = await response.json();
for (let i = 0; i < data.length; i++)
{
    this.all_accounts.push(data[i]);
}
this.loading = false;
} catch (error) {
console.error('Error fetching data:', error);
}
}
  }
}
</script>