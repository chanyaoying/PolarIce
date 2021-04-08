<template>
	<div id="app">
		<!-- start of navbar -->

		<b-navbar id="nav" toggleable="lg" type="dark" variant="">
			<div>
				<span @mouseover="hover = true" @mouseleave="hover = false">
					<b-img
						id="logo"
						src="./assets/PolarIcelogo.png"
						class="d-inline-block navBarLogo"
					>
					</b-img>
					<b-navbar-brand
						href="#"
						style="color: black; font-weight: bold; font-size: 30px"
					>
						PolarIce
					</b-navbar-brand>
				</span>
				<span v-if="hover">
					<!-- <animation /> -->

					<img id="animation" src="../src/assets/animation.gif" />
				</span>
			</div>

			<b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

			<b-collapse class="navbar-collapse" id="navbarNav" is-nav>
				<b-navbar-nav>
					<ul class="navbar-nav mr-auto" id="leftSideNav">
						<li class="b-nav-item">
							<a
								class="nav-link current"
								href="#"
								style="padding: 0px 20px; padding-bottom: unset"
								><router-link to="/">Home</router-link></a
							>
						</li>
						<li class="b-nav-item">
							<a
								class="nav-link"
								href="#"
								style="padding: 0px 20px; padding-bottom: unset"
								><router-link to="/manageRoom"
									>Manage Room</router-link
								></a
							>
						</li>
						<li class="b-nav-item">
							<a
								class="nav-link"
								href="#"
								style="padding: 0px 20px; padding-bottom: unset"
								><router-link to="/playGame"
									>Play Game</router-link
								></a
							>
						</li>
					</ul>
				</b-navbar-nav>
			</b-collapse>

			<!-- Right side -->
			<div id="navbarNavRight">
				<ul class="navbar-nav flex-row ml-auto" id="registerProfile">
					<li class="nav-item mt-1">
						<div class="dropdown">
							<b-nav-item-dropdown :text="userData.name" right>
								<b-dropdown-item href="#"
									>pid: {{ userData.pid }}</b-dropdown-item
								>
								<b-dropdown-item href="#">{{
									userData.email
								}}</b-dropdown-item>
								<b-dropdown-item @click="logout" href="#"
									><router-link to="/"
										>Sign Out</router-link
									></b-dropdown-item
								>
							</b-nav-item-dropdown>
						</div>
					</li>

					<img id="profileImage" :src="userData.profile_pic" alt="" />
				</ul>
			</div>
			<!-- End of right side -->
		</b-navbar>

		<transition name="fade" mode="out-in">
			<router-view />
		</transition>
		<!-- end of navbar -->
	</div>
</template>

<script>
import authAxios from "./components/authAxios.js";
import { mapState, mapActions } from "vuex";
// import animation from "../src/components/animation";

export default {
	// components: { animation},
	name: "allRoom",
	data: () => ({
		// userData: "",
		hover: false,
	}),
	created() {
		authAxios
			.get("https://127.0.0.1:5000/")
			.then((res) => {
				console.log("Logged in.");
				this.async_setUserData(res.data);
			})
			.catch((err) => {
				console.warn("err :>> ", err);
			});
	},
	methods: {
		...mapActions(["async_setUserData"]),
		// insert logic for method
		logout() {
			authAxios
				.get("https://127.0.0.1:5000/logout")
				.then((res) => {
					console.log("result :>> ", res);
					this.async_setUserData({});
                    if (this.$route.path !== "/") {
                        this.$router.push("/")
                    }
				})
				.catch((err) => {
					if (err.response.status === 401) {
						console.log("Unauthorised", err.response.status);
					}
                    else {
                        console.log('err :>> ', err);
                    }
				});
		},
	},
	computed: {
		...mapState(["userData"]),
	},
};
</script>

<style scoped>
@import "./styles/app.css";
</style>