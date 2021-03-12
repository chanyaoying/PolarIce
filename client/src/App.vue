<template>
    <div id="app">
        <div id="nav">
            <router-link to="/">Home</router-link> |
            <router-link to="/about">About</router-link> | 
            <router-link to= "/createRoom">createRoom</router-link>
        </div>
        <transition name="fade" mode="out-in">
            <router-view />
        </transition>
    </div>
</template>

<script>
export default {
    sockets: {
        connect(data) {
            console.log("Connect listener: " + data)
        },
        testing(data) {
            console.log("Tested socket for client! " + data);
        },
    },
};
</script>

<style scoped>
@import "./styles/app.css";
</style>