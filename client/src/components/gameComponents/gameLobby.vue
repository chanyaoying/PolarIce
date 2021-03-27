<template>
	<div>
		<h1>Game Lobby</h1>
        <h5>Waiting for game to start...</h5>
        <br>
		<b>Players:</b>
		<ul>
			<li v-for="(user, key) in users" :key="key">
				{{ user }}
			</li>
		</ul>
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
</style>