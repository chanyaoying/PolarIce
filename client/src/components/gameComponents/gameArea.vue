<template>
	<div>
		<!-- <p>game has started</p>
		<h1>Question will appear here</h1>
		<p>the choices will be here</p> -->
		<div v-if="allQuestionsViewed">
			<h1>All questions answered.</h1>
		</div>
		<Question
			:title="cachedQuestions[currentQuestion].title"
			:choices="cachedQuestions[currentQuestion].choices"
			v-else
		/>
	</div>
</template>

<script>
import Question from "./Question";
import { mapState, mapGetters ,mapActions } from "vuex";

export default {
	name: "gameArea",
	components: { Question },
	sockets: {
		nextQuestion(data) {
			this.socket_nextQuestion(data);
		},
	},
	data: () => ({}),
	methods: {
        ...mapActions(["socket_nextQuestion"])
    },
	computed: {
		...mapState(["cachedQuestions", "currentQuestion", "roomID"]),
		...mapGetters(["getLoadedQLength"]),
		allQuestionsViewed() {
			return this.getLoadedQLength === this.currentQuestion;
		},
	},
};
</script>

<style scoped>
h1 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
}
</style>