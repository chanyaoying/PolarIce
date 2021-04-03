<template>
	<div id="right">
		<hr />
		<h2>Message</h2>
		<br />
		<ul style="list-style-type:none;">
			<li v-for="(data, key) in chatHistory[roomID]" :key="key">
				{{ data }}
			</li>
		</ul>
		Send a message to the room: <br />

		<b-input-group id="message" class="mt-3">
			<b-form-input
				type="text"
				v-model="message"
				@keyup.enter="sendMessage"
				placeholder="Enter message"
			></b-form-input>
			<b-input-group-append>
				<b-button @click="sendMessage" variant="dark">
					Send Message
				</b-button>
			</b-input-group-append>
		</b-input-group>
		<br /><br />
		<!-- <p>Current Players (chat): {{ users }}</p> -->
		<br /><br />
	</div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
	name: "",
	data: () => ({ message: "" }),
	sockets: {
		receiveMessage(data) {
			this.socket_updateChat(data);
		},
	},
	methods: {
		...mapActions(["socket_updateChat"]),
		sendMessage() {
			this.$socket.client.emit("sendMessage", {
				roomID: this.roomID,
				nickname: this.nickname,
				msg: this.message,
			}); // by who
			this.message = "";
		},
	},
	computed: {
		...mapState(["chatHistory", "users", "roomID", "nickname"]),
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
	/* font-weight: bold; */
}
#right{
	background-color:white;
	/* height:500px; */
}
#message {
	width: 400px;
	margin: auto;
}
</style>