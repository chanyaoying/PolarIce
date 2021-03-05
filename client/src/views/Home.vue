<template>
    <div class="home">
        <img alt="Vue logo" src="../assets/logo.png" />
        <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
        <button @click="testing">Test</button>
    </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
    name: "Home",
    methods: {
        testing() {
            this.$socket.client.emit("testing", "Test string");
        },
    },
};
</script>
