<template>
    <div id="app">
        <b-navbar id="nav" toggleable="lg" type="dark" variant="">
            <b-navbar-brand href="#" style="color:black; font-weight:bold; font-size:40px;">
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
                <b-nav-item href="#" style="padding:0px 50px;"><router-link to="/">Home</router-link></b-nav-item>
                <b-nav-item href="#" style="padding:0px 50px;"><router-link to="/play">About</router-link></b-nav-item>
                <b-nav-item href="#" style="padding:0px 50px;"><router-link to= "/createRoom">Create Room</router-link></b-nav-item>
                <b-nav-item href="#" style="padding:0px 50px;"><router-link to= "/playGame">Play Game</router-link></b-nav-item>
            </b-navbar-nav>
            </b-collapse>
        </b-navbar>
        <transition name="fade" mode="out-in">
            <router-view />
        </transition>
    </div>
</template>

<style scoped>
    #nav{
        background-color: whitesmoke;
        height:5px;
    }
    b-nav-item{
        padding-right:100px;
        text-align: center;
    }
</style>


<script>
export default {
    // sockets: {
    //     connect(data) {
    //         console.log("Connect listener: " + data)
    //     },
    //     testing(data) {
    //         console.log("Tested socket for client! " + data);
    //     },
    // },
    // methods: {
    //     test() {
    //         this.$socket.client.emit('testing', "TEST")
    //     }
    // }
};
</script>

<style scoped>
@import "./styles/app.css";
</style>