<!--Make Websocket connections from here-->
<!-- If not connected, prompt user for name -->
<template>
	<div>
		<!-- student dont need to play music, only prof play-->
		<!-- <audio autoplay controls loop id="music">
			<source src="../assets/AreYouLost.mp3" type="audio/mpeg">
			Your browser does not support the audio element.
		</audio> -->

		<div v-if="nickname">
			<h1>Room ID: {{ roomID }}</h1>
			<br>
			<div v-if="currentComponent != 'gameArea'">
				<!-- {{currentQuestion}} -->
				
				<b-container class="bv-example-row">
					<b-row>
						<b-col>
							<component :is="currentComponent"></component>
						</b-col>
						<b-col>
							<chatBox />
						</b-col>
					</b-row>
				</b-container>

				<b-button @click="leaveRoom(nameInput)" variant="primary mt-3 mb-3">
					Leave Room
				</b-button>
			</div>
		</div>

		<div v-else>
			<h1>Room ID: {{ roomID }}</h1>
			<br />
			Please enter your name to join the room: <br />

			<b-input-group id="name" class="mt-3">
				<b-form-input
					type="text"
					v-model="nameInput"
					@keyup.enter="joinRoom(nameInput)"
					placeholder="Your nickname"
				></b-form-input>
				<b-input-group-append>
					<b-button @click="joinRoom(nameInput)" variant="dark"
						>Enter</b-button
					>
				</b-input-group-append>
			</b-input-group>
		</div>
	</div>
</template>



<script>

// document.addEventListener('click', musicPlay);
// function musicPlay() {
//     document.getElementById('music').play();
//     document.removeEventListener('click', musicPlay);
// }
import axios from "axios";
import { mapState, mapMutations, mapActions } from "vuex";
import chatBox from "../components/gameComponents/chatBox";
import gameArea from "../components/gameComponents/gameArea";
import gameLobby from "../components/gameComponents/gameLobby";


export default {
	name: "playGame",
	components: { chatBox, gameArea, gameLobby },
	sockets: {
		connect(data) {
			console.log("Users: " + data);
		},
		disconnect(data) {
			this.socket_updateChatNoRepeat(data);
		},
		join(data) {
			this.socket_updateChat(data);
		},
		leave(data) {
			this.socket_updateChat(data);
		},
		receivePlayers(data) {
			this.socket_receivePlayers(data);
		},
		changeComponent(data) {
			this.socket_changeComponent(data);
		},
	},
	data: () => ({
		nameInput: "",
	}),
	methods: {
		...mapMutations(["setRoomID"]),
		...mapActions([
			"socket_setNickname",
			"socket_updateChat",
			"socket_receivePlayers",
			"socket_updateChatNoRepeat",
			"socket_changeComponent",
		]),
		joinRoom(nameInput) {
			this.$socket.client.emit("join", {
				roomID: this.roomID,
				username: nameInput,
			});
			console.log("you have joined the room!");
			// set nickname in vuex
			this.socket_setNickname(nameInput);
		},
		leaveRoom(nameInput) {
			this.$socket.client.emit("leave", {
				roomID: this.roomID,
				username: nameInput,
			});
			this.socket_setNickname("");
		},
	},
	computed: {
		...mapState(["nickname", "roomID", "currentComponent"]),
		
		currentQuestion(){
			return this.$store.getters.GetCurrentQuestion;
		}
	},
	created() {
		this.setRoomID(this.$route.params.roomID);
		axios
			.get("http://127.0.0.1:5001/live?roomID=" + this.roomID)
			.then((res) => {
				if (!res.data.live) {
					// room is not live
					this.$router.push("/playGame");
				}
			})
			.catch((err) => {
				console.log("err :>> ", err);
			});
	},
};
</script>

<style scoped>
h1 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
}
#name {
	width: 400px;
	margin: auto;
}

#start {
	position: fixed;
	bottom: 15px;
	right: 15px;
}
#music{
	width: 20%;
	margin-top: 10px;
	margin-left: 75%;
}

</style>