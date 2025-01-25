<template>
    <div id="app">
        <SessionExpiredNotification
            v-if="eventBus.showSessionNotification"
            @close="eventBus.showSessionNotification = false"
        />
        <router-view />
    </div>
</template>

<script>
import { eventBus } from './utils/eventBus';
import SessionExpiredNotification from './components/others/SessionExpiredNotification.vue';

export default {
  name: "App",
  components: {
    SessionExpiredNotification,
  },
  data() {
    return {
      showSessionNotification: false,
    };
  },
  computed: {
        eventBus() {
            return eventBus;
        }
      },
};
</script>
<style scoped>

footer {
    display: block;
    color: aqua;
    text-align: center;
    padding: 20px 0;
    bottom: 0;
    width: 100%;
}
</style>