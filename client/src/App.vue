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

            <b-collapse class="collapse navbar-collapse " id="navbarNav">
                <ul class="navbar-nav mr-auto" id="leftSideNav">
                    <li class="b-nav-item">
                        <a class="nav-link current" href="#" style="padding:0px 20px;padding-bottom:unset;"><router-link to="/">Home</router-link></a>
                    </li>
                    <li class="b-nav-item">
                        <a class="nav-link" href="#" style="padding:0px 20px; padding-bottom:unset;"><router-link to= "/createRoom">Create Room</router-link></a>
                    </li>
                    <li class="b-nav-item">
                        <a class="nav-link" href="#" style="padding:0px 20px;padding-bottom:unset;"><router-link to= "/playGame">Play Game</router-link></a>
                        </li>
                </ul>
            </b-collapse>

        <!-- Right side -->
        <div id="navbarNavRight">
            <ul class="navbar-nav flex-row ml-auto" id="registerProfile">
                <li class="nav-item mt-1" >
                    <div class="dropdown">
                        <b-nav-item-dropdown :text= "userData.name" right>
                            <b-dropdown-item href="#">{{ userData.email }}</b-dropdown-item>
                            <b-dropdown-item @click="logout" href="#"><router-link to="/">Sign Out</router-link></b-dropdown-item>
                        </b-nav-item-dropdown>
                    </div>
                </li>
                 
                <img id="profileImage" :src="userData.profile_pic" alt="" /> 
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
import authAxios from './components/authAxios.js';
export default {
    name: "allRoom",
    data: () => ({
        userData: "",
    }),
    created() {
        authAxios
            .get("https://127.0.0.1:5000/")
            .then((res) => {
                console.log("result :>> ", res);
                this.userData = res.data;
            })
            .catch((err) => {
                console.log("err :>> ", err);
            });
    },
    methods: {
        // insert logic for method
        logout(){
           authAxios
            .get("https://127.0.0.1:5000/")
            .then((res) => {
                console.log("result :>> ", res);
                this.userData = false;
            })
        }
    }
};
</script>

<style scoped>
@import "./styles/app.css";
</style>
