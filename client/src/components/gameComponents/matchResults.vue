<template>
	<div>
		<b-container style="width: 70%">
			<b-card>
				<b-img id="bear" src="../../assets/bear.gif"></b-img>
				<h2>Your best friends are:</h2>
				<p>{{ matchResults }}</p>
				<br />
			</b-card>
		</b-container>
	</div>
</template>

<style scoped>
h1 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
}
h2 {
	font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
		sans-serif;
}
#bear {
	width: 30%;
}
</style>

<script>
import { mapState } from "vuex";

export default {
	name: "matchResults",
	data: () => ({}),
	methods: {},
	computed: {
		...mapState(["matchResults"]),
	},
	created() {},
};
</script>