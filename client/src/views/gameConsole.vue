<template>
	<div>
		<h1>Console: {{ roomID }}</h1>
		<p>Control the game from the prof's point of view</p>
		<div v-if="started">
			<b-button class="btn-lg" id="next" variant="primary" @click="nextQuestion" v-if="!allQuestionsViewed">Next</b-button>
			<b-button class="btn-lg" id="end" variant="danger" @click="endGame"
				>End</b-button
			>
		</div>

		<b-button
			class="btn-lg"
			id="start"
			variant="success"
			@click="startGame"
			v-else
			>Start</b-button
		>

		<br />
		<component :is="currentComponent"></component>
	</div>
</template>

<script>
// TODO:
// Make sure that this page can only be accessed when authenticated. i.e. the prof OWNS the room.

import { mapState, mapMutations, mapActions } from "vuex";
import gameLobby from "../components/gameComponents/gameLobby";
import gameArea from "../components/gameComponents/gameArea";
import axios from "axios";

export default {
	name: "gameConsole",
	components: { gameLobby, gameArea },
	sockets: {
		receivePlayers(data) {
			this.socket_receivePlayers(data);
		},
		changeComponent(data) {
			this.socket_changeComponent(data);
		},
	},
	data: () => ({
		started: false,
	}),
	methods: {
		...mapMutations(["setRoomID"]),
		...mapActions(["socket_receivePlayers", "socket_changeComponent"]),
		startGame() {
			this.started = true;
			// send authenticated socket emit to start game
			// for now, just a normal socket emit to start game
			this.$socket.client.emit("startGame", {
				roomID: this.roomID,
			});
		},
		endGame() {
			this.started = false;
			// needs to be authenticated
			this.$socket.client.emit("endGame", {
				roomID: this.roomID,
			});
		},
		nextQuestion() {
			this.$socket.client.emit("nextQuestion", {
				roomID: this.roomID,
				currentQuestionNumber: this.currentQuestion
			})
		},
	},
	computed: {
		...mapState(["currentComponent", "users", "roomID", "loadedQuestions", "currentQuestion"]),
		allQuestionsViewed() {
			return this.loadedQuestions.length === this.currentQuestion;
		},
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
		// check if user is authenticated
		// if user is authenticated, prof joins room
		this.$socket.client.emit("join", {
			roomID: this.roomID,
			username: "gameMaster",
			gameMaster: true,
		});
	},
};
</script>

<style scoped>
</style>