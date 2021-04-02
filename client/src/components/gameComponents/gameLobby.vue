<template>
	<div id="left">
		<b-card>
		<h2>Game Lobby</h2>
        <h6>Waiting for game to start...</h6>
        <br>
		<b>Players:</b>
		<ul style="list-style-type:none;">
			<li v-for="(user, key) in users" :key="key">
				{{ user }}
			</li>
		</ul>

		<br>
		</b-card>
	</div>
</template>

<script>
import { mapState } from "vuex";

export default {
	name: "gameLobby",
	data: () => ({}),
	methods: {},
	computed: {
		...mapState(["users"]),
	},
};
</script>

<style scoped>
h1 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	font-weight: bold;
}
h2{
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;

}
#left{
	/* background-color:white; */
	/* height:500px; */
}
</style>