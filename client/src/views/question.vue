<!--Make Websocket connections from here-->
<!-- If not connected, prompt user for name -->
<template>
    <div>
        <h1>Room ID: {{ roomID }}</h1>
        <div id="question">
            <h2>Question: Are you a cat person or a dog person?</h2>
        </div>
        <div class="choice">
            <div class="col-md-12 text-center">
                <b-form>
                    <b-button class="choice1 btn-lg" variant="warning">Cat </b-button>
                    <b-button class="choice1 btn-lg" variant="primary">Dog </b-button>
                </b-form>
            </div>
        </div>

        <b-button id="next" variant="success">Next</b-button>
    </div>
</template>

<style scoped>
    h1{
        margin-top: 10px;
        font-family: Arial, Helvetica, sans-serif;
        font-weight: bold;
    }
    #question{
        margin-top: 50px;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }
    #next{
        margin-top: 12%; 
        float:right; 
        position: relative;
        margin-right: 2%;
    }
    .choice1{
        margin: 100px 50px 0px 50px;
        width: 400px;
       
    }
</style>

<script>
import axios from "axios";

export default {
    name: "question",
    sockets: {
        connect(data) {
            console.log("Users: " + data);
        },
        disconnect(data) {
            console.log("Users: " + data);
        },
        join(data) {
            // receive from server
            console.log("data :>> ", data);
        },

    },
    data: () => ({
        message: "",
        chatHistory: [],
    }),
    methods: {
    },
    computed: {
        roomID() {
            return this.$route.params.roomID;
        },
    },
    created() {
        // Check if room is live
        // While checking, the client will be briefly connected to the websocket before being redirected.
        // Huge security concern, but not within the scope of this course.
        // If we were to fix this, we would not use asynchronous checking.
        axios
            .get("http://127.0.0.1:5001/live?roomID=" + this.roomID)
            .then((res) => {
                if (!res.data.live) {
                    this.$router.push("/question");
                }
            })
            .catch((err) => {
                console.log("err :>> ", err);
            });
    },
};
</script>