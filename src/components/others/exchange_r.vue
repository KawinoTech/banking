<template>
<div>
    <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-inner" style="color:aqua; padding: 20px;">
        <div class="carousel-item active">
            <p>EXCHANGE RATES</p>
        </div>
        <div class="carousel-item" v-for="cur in currencies" :key="cur">
            <p>{{ cur.curr }}
                <i class="fa-solid fa-arrow-up" v-if="cur.variance > 0"
                    style="color: green; margin-right: 3px;"></i>
                <i class="fa-solid fa-arrow-down" v-else-if="cur.variance < 0"
                style="color: red; margin-right: 3px;"></i>
                <i class="fa-solid fa-minus" v-else style="color: white; margin-right: 3px;"></i>{{ cur.current }}
            </p>
        </div>
    </div>
</div>
</div>
</template>
<script>
import json from '../../assets/exchange-rates.json'

export default {
  name: 'Currencies_Trend',

     data(){
        return {
            loading: true,
            currencies: []
        };
     },

     mounted() {
        this.apendJson();
    },

  methods: {
    async fetchData() {
        try {
            const response = await fetch('');
            const data = await response.json();
            for (let i = 0; i < data.currencies.length; i++)
            {
                this.currencies.push(data.currencies[i]);
            }
            this.loading = false;
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    },
    apendJson() {
                try {
            for (let i = 0; i < json.currencies.length; i++)
            {
                this.currencies.push(json.currencies[i]);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
  }
}
</script>