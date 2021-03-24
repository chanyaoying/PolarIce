<template>
	<div>
		<p>game has started</p>
		<h1>Question will appear here</h1>
		<p>the choices will be here</p>
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
	},
	data: () => ({}),
	methods: {
        ...mapActions(["socket_nextQuestion"])
    },
	computed: {
		...mapState(["loadedQuestions", "currentQuestion"]),
		allQuestionsViewed() {
			return this.loadedQuestions.length === this.currentQuestion;
		},
	},
};
</script>

<style scoped>
</style>