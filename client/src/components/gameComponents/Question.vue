<template>
	<b-container>
	<b-card id="ques">
	<div v-if="!clicked">
		<div id="question">
			<h2>{{ title }}</h2>
		</div>
		<div class="choice">
			<div class="col-md-12 text-center">
				<b-form>
					<b-button
						class="choice1 btn-lg"
						variant="primary"
						v-for="(choice, key) in splitChoices"
						:key="key"
						@click="onSelect(choice)"
						>{{choice}}
					</b-button>
				</b-form>
			</div>
		</div>
		
	</div>
	<div id="question" v-else>
		<h2>Answer Submited! Please wait for the next question.</h2>
	</div>
	</b-card>
	</b-container>
</template>

<script>
import { mapState } from "vuex";

export default {
	name: "question",
	props: ["title", "choices"],
	sockets: {},
	data: () => ({
		select: [],
		clicked: false
	}),
	methods: {
		onSelect(choice){
			this.select.push(choice);
			this.clicked = true
			console.log(this.select);
			if (this.clicked === this.$store.getters.getLoadedQLength){
				console.log("last question, pushing to state.");
				this.$store.commit('addCollectedResult',this.select);
				console.log(this.$store.state.collectedResult);
			}
		}
	},
	computed: {
		...mapState(["currentQuestion"]),
		splitChoices() {
			return this.choices.split("/")
		},
	},
	watch: {
		currentQuestion: function () {
			this.clicked = false
		}
	}
};
</script>

<style scoped>
h1 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
}
#question {
	/* margin-top: 10px; */
	font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
		sans-serif;
}
#next {
	margin-top: 12%;
	float: right;
	position: relative;
	margin-right: 2%;
}
.choice1 {
	margin: 70px 50px 20px 50px;
	/* width:400px; */
	width: 40%;
}
#ques{
	height: 400px;
}
</style>