<!--Make Websocket connections from here-->
<!-- If not connected, prompt user for name -->
<template>
	<div>

		<div v-if="nickname">
			<h1>PIN: {{ roomID }}</h1>
			<br />
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

				<b-button
					@click="leaveRoom(nameInput)"
					variant="primary mt-3 mb-3"
				>
					Leave Room
				</b-button>
			</div>
			<div v-else>
				<component :is="currentComponent"></component>
				<b-button
					@click="leaveRoom(nameInput)"
					variant="primary mt-3 mb-3"
				>
					Leave Room
				</b-button>
			</div>
		</div>

		<div v-else>
			<h1>PIN: {{ roomID }}</h1>
			<br />
			Please enter your name to join the room: <br />

			<b-input-group id="name" class="mt-3">
				<b-form-input
					type="text"
					v-model="nameInput"
					@keyup.enter="joinRoom(nameInput)"
					placeholder="Your nickname"
					:state="nameInput !== ''"
					aria-describedby="input-live-feedback"
				></b-form-input>
				<b-input-group-append>
					<b-button @click="joinRoom(nameInput)" variant="dark"
						>Enter</b-button
					>
				</b-input-group-append>
			</b-input-group>

			<b-form-invalid-feedback id="input-live-feedback">
				Please enter something!
			</b-form-invalid-feedback>
		</div>
	</div>
</template>



<script>

import axios from "axios";
import { mapState, mapMutations, mapActions } from "vuex";
import chatBox from "../components/gameComponents/chatBox";
import gameArea from "../components/gameComponents/gameArea";
import gameLobby from "../components/gameComponents/gameLobby";
import matchResults from "../components/gameComponents/matchResults"

export default {
	name: "playGame",
	components: { chatBox, gameArea, gameLobby, matchResults },
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
		getQuestions(data) {
			this.socket_getQuestions(data);
		},
		endGame(data) {
			if (data) {
				// send data up to the server
				console.log("this.playerChoices :>> ", this.playerChoices);
				this.$socket.client.emit("sendResult", {
					roomID: this.roomID,
					nickname: this.nickname,
					results: this.playerChoices,
				});
			}
		},
		getMatching(data) {
			if (data) {
				// send nickname up to the server
				this.$socket.client.emit("matchingResult", {
					nickname: this.nickname,
					roomID: this.roomID,
				})
			}
		},
		matchingResult(data) {
			if (data) {
				this.socket_setMatchResults(data)
			}
			else {
				console.warn('Failed.', data);
			}
		}
	},
	data: () => ({
		nameInput: "",
		state: null,
	}),
	methods: {
		...mapMutations(["setRoomID"]),
		...mapActions([
			"socket_setNickname",
			"socket_updateChat",
			"socket_receivePlayers",
			"socket_updateChatNoRepeat",
			"socket_changeComponent",
			"socket_getQuestions",
			"socket_setMatchResults",
		]),
		joinRoom(nameInput) {
			if (nameInput === "") {
				alert("Please enter something!");
			} else {
				this.$socket.client.emit("join", {
					roomID: this.roomID,
					username: nameInput,
				});
				// set nickname in vuex
				this.socket_setNickname(nameInput);
			}
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
		...mapState([
			"nickname",
			"roomID",
			"currentComponent",
			"playerChoices",
			"nickname",
		]),

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
#music {
	width: 20%;
	margin-top: 10px;
	margin-left: 75%;
}
</style>