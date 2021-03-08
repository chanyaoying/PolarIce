<template>
    <div class="about">
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
