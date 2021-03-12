<template>
    <div id="app">
        <div id="nav">
            <router-link to="/">Home</router-link> |
            <router-link to="/play">About</router-link> | 
            <router-link to= "/createRoom">createRoom</router-link> | 
            <router-link to= "/playGame">Play Game</router-link>
            <!-- <p @click="test">test</p> -->
        </div>
        <transition name="fade" mode="out-in">
            <router-view />
        </transition>
    </div>
</template>

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