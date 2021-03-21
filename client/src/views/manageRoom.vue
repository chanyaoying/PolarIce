<template>
    <div>
        <br><br>
            <b-card-group deck id="card-group">
                <b-card>
                <b-card-header>
                    Welcome, {{ userData.name }}
                </b-card-header>
                <b-card-text id="room1">Let's get started:</b-card-text>
                <b-row>
                <b-card id = "card">
                    <b-avatar :src="require('../assets/game.png')" size="6rem"></b-avatar>
                    <b-button href="#" variant="dark" id="button">Play Game</b-button>
                </b-card>
                <b-card id = "card">
                    <b-avatar :src="require('../assets/create.png')" size="6rem"></b-avatar>
                    <b-button href="#" variant="dark" id="button">Create Room</b-button>
                </b-card>
                <b-card id = "card">
                    <b-avatar :src="require('../assets/edit.png')" size="6rem"></b-avatar>
                    <b-button href="#" variant="dark" id="button">Edit Room</b-button>
                </b-card>
                </b-row>
                </b-card>
            </b-card-group>
        <br><br>

        <b-card-group deck id="card-group">
            <b-card
                header="Rooms"
                header-tag="header"
                footer="PolarIce"
                footer-tag="footer"              
            >
            <b-col>
                <b-link id="link" href="#foo">Room: ESD Room 1</b-link>
            </b-col>
            <b-col>
                <b-link id="link" href="#foo">Room: ESD Room 2</b-link>
            </b-col>
            <b-col>
                <b-link id="link" href="#foo">Room: ESD Room 3</b-link>
            </b-col>
            <b-col id="col">
                <b-link id="link" href="#foo">Room: ESD Room 4</b-link>
            </b-col>      
            </b-card>
        </b-card-group>
        <br><br>
    </div>    
</template>

<style scoped>
    #card-group{
        width:50%;
        margin: auto;
    }
    #button{
        margin-top:10px
    }
    #room{
        font-size: large;
    }
    #card{
        width: 30%;
    }
    #room1{
        text-align: left;
        font-size: large;
    }
    #create1{
        margin-right:10px;
    }
    #col{
        margin-bottom:20px;
    }
    #link{
        font-size:20px;
    }
</style>

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