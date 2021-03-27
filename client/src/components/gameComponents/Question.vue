<template>
	<div>
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
						>{{choice}}
					</b-button>
				</b-form>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "question",
	props: ["title", "choices"],
	sockets: {},
	data: () => ({}),
	methods: {},
	computed: {
		splitChoices() {
			return this.choices.split("/")
		}
	},
};
</script>

<style scoped>
h1 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
}
#question {
	margin-top: 50px;
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
	margin: 100px 50px 0px 50px;
	width: 400px;
}
</style>