<template>
	<div id="right">
		<b-card>
			<h2>Message</h2>
			<p v-if="banned" id="banned">
				You have been banned from chatting for 30 seconds.
			</p>
			<br />
			<div class="scroll">
				<ul style="list-style-type: none">
					<li
						v-for="(data, key) in chatHistory[roomID]"
						:key="key"
						style="text-align: left"
					>
						<div class="profword" v-if="data[0] == ':'">
							{{ systemMessage(data) }}
						</div>
						<div v-else>
							{{ data }}
						</div>
					</li>
				</ul>
			</div>
			Send a message to the room: <br />

			<b-input-group id="message" class="mt-3">
				<b-form-input
					type="text"
					v-model="message"
					@keyup.enter="sendMessage"
					placeholder="Enter message"
					v-if="!banned"
				></b-form-input>
				<b-form-input
					v-if="banned"
					placeholder="You have been banned."
					readonly
				></b-form-input>
				<b-input-group-append>
					<b-button
						@click="sendMessage"
						v-if="!banned"
						variant="dark"
					>
						Send Message
					</b-button>
				</b-input-group-append>
			</b-input-group>
			<br />
		</b-card>
	</div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
	name: "",
	data: () => ({
		message: "",
		banned: false,
		recentMessages: [],
	}),
	sockets: {
		receiveMessage(data) {
			this.socket_updateChat(data);
		},
	},
	methods: {
		...mapActions(["socket_updateChat"]),
		sendMessage() {
			if (this.message !== "") {
				this.$socket.client.emit("sendMessage", {
					roomID: this.roomID,
					nickname: this.nickname,
					msg: this.message,
				}); // by who
				this.recentMessages.push(this.message);
				this.message = "";
			}
		},
		scrollToEnd() {
			var container = document.querySelector(".scroll");
			var scrollHeight = container.scrollHeight;
			container.scrollTop = scrollHeight;
		},
		systemMessage(word) {
			return word.slice(1);
		},
	},
	mounted() {
		this.scrollToEnd();
		// banning
		let counter = 0;
		setInterval(() => {
			if (this.recentMessages.length > 2) {
				this.banned = true;
				this.$socket.client.emit("sendMessage", {
					roomID: this.roomID,
					nickname: '',
					msg: `${this.nickname} has been banned for 30 seconds for spamming.`,
				});
			} else {
				counter += 1;
				if (counter == 15) {
					this.banned = false;
					counter = 0;
				}
			}
			this.recentMessages = [];
		}, 2000);
	},
	updated() {
		this.scrollToEnd();
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
h2 {
	margin-top: 10px;
	font-family: Arial, Helvetica, sans-serif;
	/* font-weight: bold; */
}
/* #right{
	background-color:white; 
	height : 300px;
	height:500px; 
} */
#message {
	width: 400px;
	margin: auto;
	align-content: left;
}
#banned {
	color: red;
}
.scroll {
	margin: auto;
	width: 90%;
	max-height: 150px;
	overflow: scroll;
	margin-bottom: 20px;
}
.profword {
	color: red;
}
</style>