<template>
	<div>
		<audio autoplay controls loop id="music">
			<source src="../assets/AreYouLost.mp3" type="audio/mpeg">
			Your browser does not support the audio element.
		</audio>
		<h1>Console: {{ roomID }}</h1>
		<p>Control the game from the prof's point of view</p>
	
		<div v-if="started">
			<b-button class="btn-lg" id="next" variant="success" @click="nextQuestion" v-if="!allQuestionsViewed">Next</b-button>
			<b-button class="btn-lg" id="end" variant="danger" @click="endGame">End</b-button>
				<br><br>
				<component :is="currentComponent"></component>
		</div>

		<div v-else>		
			<b-button class="btn-lg" id="start" variant="success" @click="startGame">
				Start
			</b-button>

			<b-container id = "container" class="bv-example-row">
			<b-row>
				<b-col><br>
					<component :is="currentComponent"></component>
				</b-col>
				<b-col><br>
					<chatBox />
				</b-col>
			</b-row>
		</b-container>

		</div>
		<br />

	</div>
</template>

<script>
document.addEventListener('click', musicPlay);
function musicPlay() {
    document.getElementById('music').play();
    document.removeEventListener('click', musicPlay);
}
// TODO:
// Make sure that this page can only be accessed when authenticated. i.e. the prof OWNS the room.

import { mapState, mapMutations, mapActions } from "vuex";
import gameLobby from "../components/gameComponents/gameLobby";
import gameArea from "../components/gameComponents/gameArea";
import chatBox from "../components/gameComponents/chatBox";
import axios from "axios";

export default {
	name: "gameConsole",
	components: { gameLobby, gameArea ,chatBox},
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
h1 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
}
#music{
	width: 20%;
	margin-top: 10px;
	margin-left: 75%;
}
#next{
	margin-right:10px;
}
</style>