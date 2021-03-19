<template>
    <div id="app">
        <!-- start of navbar -->
        <b-navbar id="nav" toggleable="lg" type="dark" variant="">
            <b-img src="./assets/PolarIcelogo.png" class="d-inline-block navBarLogo" > </b-img>
            <b-navbar-brand href="#" style="color:black; font-weight:bold; font-size:30px;">
                PolarIce
            </b-navbar-brand>
            <!-- <router-link to="/">Home</router-link> | 
            <router-link to="/play">About</router-link> | 
            <router-link to= "/createRoom">createRoom</router-link> | 
            <router-link to= "/playGame">Play Game</router-link> -->
            <!-- <p @click="test">test</p> -->
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item href="#" style="padding:0px 20px;"><router-link to="/">Home</router-link></b-nav-item>
                    <b-nav-item href="#" style="padding:0px 20px;"><router-link to= "/createRoom">Create Room</router-link></b-nav-item>
                    <b-nav-item href="#" style="padding:0px 20px;"><router-link to= "/playGame">Play Game</router-link></b-nav-item>
                </b-navbar-nav>
            </b-collapse>

        <!-- Right side -->
        <div id="navbarNavRight">
            <ul class="navbar-nav flex-row ml-auto" id="registerProfile">
              <li class="nav-item mt-2 mr-1" id="change">
                <!-- Search bar -->
                <search-component></search-component>
             </li>
             <div id="profilePic">
                <!-- Replace me with Sign in or Profile -->
                <!-- <b-img :src="userData.profile_pic" class="d-inline-block navBarLogo" > </b-img> -->
             </div>
            </ul>
        </div>
        <!-- End of right side -->

        </b-navbar>

        <transition name="fade" mode="out-in">
            <router-view />
        </transition>

        
        
        <!-- end of navbar -->

    </div>
</template>


<script>
export default {};
</script>

<style scoped>
@import "./styles/app.css";
</style>