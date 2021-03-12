<template>
    <div>
        <button @click="createRoom()">Create Room</button>
        <h1>Welcome, {{ userData.name }}</h1>
        <p>{{ userData.email }}</p>
        <img :src="userData.profile_pic" alt="" />
    </div>
</template>

<script>
import authAxios from '../components/authAxios.js';
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
    }
};
</script>