    <template>    
        <div class="container-lg">
            <div class="justify-content-center align-items-center">
                <div>
                    <!--Navigation Bar Contains GT Logo, Search bar, Notification icon and profile picture update-->
                    <nav class="navbar navbar-light fixed-top navbar-expand-xl mb-3" style="background-color: white;">
                        <a href="#" class="navbar-brand mb-0 h1">
 <router-link to="/home"><img src="../assets/logo.png" alt="Logo" width="30" height="24" class="d-inline-block align-text-top"></router-link>
                            Vue JS
                        </a>
                        <!-- Toggles the navbar when screen size reduces
                        data-bs-toggle - invokes the navbar when button is pressed
                        data-bs-target - targets the navbar specified by its id -->
                        <button class="navbar-toggler" type="button" data-bs-target="#navbarNav" 
                        data-bs-toggle="collapse" aria-expanded="false" aria-controls="navbarNav" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul class="navbar-nav">
                                <li class="nav-item active m-2">
                                    <a href="#" class="nav-link"><i class="fa-regular fa-user"></i>My Account</a>
                                </li>
                            </ul>
                            <ul class="navbar-nav">
                                <li class="nav-item active m-2">
                                    <router-link to="/customer_service" style="text-decoration: none;"><i class="fa-solid fa-circle-info"></i>Customer Care</router-link>
                                </li>
                            </ul>
                            <ul class="navbar-nav m-2">
                                <li class="nav-item active">
                                    <router-link to="/report_problem" style="text-decoration: none;"><i style="color: red" class="fa-solid fa-circle-exclamation fa-beat"></i>Report Problem</router-link>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
    </template>
    <script>
    export default {
        name: 'Nav_Bar',
        emits: ['close'],
        data() {
            return {
                data1: "Hello"
            }
        }
    }
    
</script>
<style scoped>
i {
    margin-right: 5px;
    font-size: large;
    text-decoration: none;
}
</style>