<template>
	<div>
		<!-- <p>game has started</p>
		<h1>Question will appear here</h1>
		<p>the choices will be here</p> -->
		<div v-if="allQuestionsViewed">
			<h1>All questions answered.</h1>
		</div>
		<Question
			:title="loadedQuestions[currentQuestion].title"
			:choices="loadedQuestions[currentQuestion].choices"
			v-else
		/>
	</div>
</template>

<script>
import Question from "./Question";
import { mapState, mapActions } from "vuex";

export default {
	name: "gameArea",
	components: { Question },
	sockets: {
		nextQuestion(data) {
			this.socket_nextQuestion(data);
		},
        getQuestions(data) {
            this.socket_getQuestions(data);
        }
	},
	data: () => ({}),
	methods: {
        ...mapActions(["socket_nextQuestion", "socket_getQuestions"])
    },
	computed: {
		...mapState(["loadedQuestions", "currentQuestion", "roomID"]),
		allQuestionsViewed() {
			return this.loadedQuestions.length === this.currentQuestion;
		},
	},
    created() {
        // get game data
        this.$socket.client.emit("getQuestions", {
            roomID: this.roomID
        });
    }
};
</script>

<style scoped>
h1 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
}
</style>