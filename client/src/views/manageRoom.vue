<template>
	<div>
		<br /><br />
		<b-card-group deck id="card-group">
			<b-card>
				<b-card-header> Welcome, {{ userData.name }} </b-card-header>
				<b-card-text id="room1">Let's get started:</b-card-text>
				<b-row>
					<b-card id="card">
						<b-avatar
							:src="require('../assets/game.png')"
							size="6rem"
						></b-avatar>
						<b-button href="#" variant="dark" id="button"
							><router-link class="buttontext" to="/playGame"
								>Play Game</router-link
							></b-button
						>
					</b-card>
					<b-card id="card">
						<b-avatar
							:src="require('../assets/create.png')"
							size="6rem"
						></b-avatar>
						<b-button href="#" variant="dark" id="button"
							><router-link class="buttontext" to="/createRoom"
								>Create Room</router-link
							></b-button
						>
					</b-card>
					<b-card id="card">
						<b-avatar
							:src="require('../assets/edit.png')"
							size="6rem"
						></b-avatar>
						<b-button
							variant="dark"
							id="button"
							@click="$bvModal.show('bv-modal')"
							>Edit Room</b-button
						>

						<b-modal id="bv-modal" hide-footer>
							<template #modal-title>
								Sorry. We are still working on this function.
							</template>
							<b-img
								id="us"
								class="my-2"
								src="../assets/us.jpg"
							></b-img>
							<b-button
								class="mt-3"
								block
								@click="$bvModal.hide('bv-modal')"
								>Close Me</b-button
							>
						</b-modal>
					</b-card>
				</b-row>
			</b-card>
		</b-card-group>
		<br /><br />

		<b-card-group deck id="card-group">
			<b-card
				header="Rooms"
				header-tag="header"
				footer="PolarIce"
				footer-tag="footer"
			>
				<b-col v-for="(question, key) in questions" :key="key">
					<b-link id="link" @click="loadRoom(question)">Room {{question}}</b-link>
				</b-col>
			</b-card>
		</b-card-group>
		<br /><br />
	</div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import authAxios from "../components/authAxios";
import axios from "axios";

export default {
	name: "allRoom",
	data: () => ({
		questions: [],
	}),
	methods: {
		...mapActions(["async_setUserData"]),
		loadRoom(rID) {
			authAxios
				.get(`https://127.0.0.1:5000/load?roomID=${rID}`)
				.then((res) => {
					this.$router.push(res.data)
				})
				.catch((err) => {
					console.warn("err :>> ", err);
				});
		},
	},
	computed: {
		...mapState(["userData"]),
	},
	created() {
		authAxios
			.get("https://127.0.0.1:5000/")
			.then((res) => {
				this.async_setUserData(res.data);
			})
			.catch((err) => {
				console.log("err :>> ", err);
				// not logged in
				this.$router.push("/404_notLoggedIn");
			});
		// get all rooms
		axios.get("http://127.0.0.1:5004/rooms").then(res => {
			console.log('res :>> ', res);
			// display rooms
			this.questions = res.data
		}).catch(err => {
			console.warn('err :>> ', err);
		})
	},
};
</script>

<style scoped>
#card-group {
	width: 50%;
	margin: auto;
}
#button {
	margin-top: 10px;
}
#room {
	font-size: large;
}
#card {
	width: 30%;
}
#room1 {
	text-align: left;
	font-size: large;
}
#create1 {
	margin-right: 10px;
}
#col {
	margin-bottom: 20px;
}
#link {
	font-size: 20px;
}
.buttontext {
	color: white;
}
#us {
	display: block;
	margin-left: auto;
	margin-right: auto;
	width: 80%;
}
</style>