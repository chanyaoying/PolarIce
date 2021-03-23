<template>
	<div>
		<h1>Console: {{roomID}}</h1>
		<p>Control the game from the prof's point of view</p>
		<b-button class="btn-lg" id="start" variant="success">Start</b-button>
		<br />
		<component :is="currentComponent"></component>
	</div>
</template>

<script>
// TODO:
// Make sure that this page can only be accessed when authenticated. i.e. the prof OWNS the room.

import { mapState, mapMutations } from "vuex";
import gameLobby from "../components/gameComponents/gameLobby";

export default {
	name: "gameConsole",
	components: { gameLobby },
	sockets: {
		receivePlayers(data) {
			this.socket_receivePlayers(data);
		},
	},
	data: () => ({}),
	methods: {
        ...mapMutations(["setRoomID"]),
    },
	computed: {
		...mapState(["currentComponent", "users", "roomID"]),
	},
    created() {
        this.setRoomID(this.$route.params.roomID);
    }
};
</script>

<style scoped>
</style>