<template>
	<div class="room">
		<div class="card" style="margin: 20px auto; width: 90%">
			<div class="card-body">
				<b-row>
					<b-col
						><b-button variant="success" @click="done()"
							>Done</b-button
						></b-col
					>
				</b-row>

				<b-container id="fluid">
					<b-row>
						<b-col>
							<b-row>
								<!-- create own question -->
								<div>
									<b-card
										id="selfquestion"
										class="mt-3"
										header="Create your own Question:"
									>
										<b-form>
											<b-form-group id="input-group-1">
												<b-form-input
													v-model="newQ.question"
													placeholder="Enter your question."
													required
												></b-form-input>
												<b-form-input
													v-model="newQ.choice1"
													placeholder="Enter choice 1"
													required
												></b-form-input>
												<b-form-input
													v-model="newQ.choice2"
													placeholder="Enter choice 2"
													required
												></b-form-input>
											</b-form-group>

											<b-button
												variant="primary"
												@click="onSubmit"
												class="mr-4"
												>Submit</b-button
											>
											<b-button
												variant="danger"
												@click="onReset"
												>Reset</b-button
											>
										</b-form>
									</b-card>
								</div>
							</b-row>

							<b-row>
								<!-- Random questions -->
								<b-card
									class="mt-3"
									id="selfquestion"
									header="You can choose to use the following questions (optional):"
								>
									<div class="ml-4">
										<ol>
											<li
												style="text-align: left"
												v-for="(
													firebasedb, i
												) in firebase"
												:key="i"
											>
												<b-row>
													<b-col cols="10">
														
														<span
															><b>Question:</b>
															{{
																firebasedb.title
															}}</span
														><br />
														<span
															><b>Choices:</b>
															{{
																firebasedb.choices
															}}</span
														>
													</b-col>
													<b-col>
														<b-button
															variant="warning"
															@click="
																add(firebasedb,i)
															"
															>Add</b-button
														>
													</b-col>
												</b-row>
												<hr />
											</li>
										</ol>
									</div>
								</b-card>
							</b-row>
						</b-col>
						<b-col>
							<b-card class="mt-3" header="Added Question">
								<ol class="ml-3">
									<li
										style="text-align: left"
										v-for="(
											addedQuestion, i
										) in question_list"
										:key="i"
									>
										<b-row>
											<b-col cols="9">
												<span
													><b>Question:</b>
													{{
														addedQuestion.title
													}}</span
												><br />
												<span
													><b>Choices:</b>
													{{
														addedQuestion.choices
													}}</span
												>
											</b-col>
											<b-col>
												<b-button
													variant="danger"
													@click="
														remove(addedQuestion,i)
													"
													>Remove</b-button
												>
											</b-col>
										</b-row>
										<hr />
									</li>
								</ol>
							</b-card>
						</b-col>
					</b-row>
				</b-container>
			</div>
		</div>
	</div>
</template>

<script>
import authAxios from "../components/authAxios";
import { mapState } from "vuex";

export default {
	name: "room",
	data: () => ({
		createdRoomID: false,
		// roomID:'',
		firebase: [],
		question_list: [],
		newQ: {
			question: "",
			choice1: "",
			choice2: "",
		},
	}),
	mounted:function(){
		this.getDataFromFirebase();
	},
	methods: {
		onSubmit() {
			this.question_list.push({
				title: this.newQ.question,
				choices: this.newQ.choice1
					.concat("/")
					.concat(this.newQ.choice2),
				dbsrc: "user", // userid, to store in DB
			});
			this.newQ.question = "";
			this.newQ.choice1 = "";
			this.newQ.choice2 = "";
		},
		onReset() {
			this.newQ.question = "";
			this.newQ.choice1 = "";
			this.newQ.choice2 = "";
		},
		add(firebasedb,i) {
			this.question_list.push(firebasedb);
			this.firebase.splice(i, 1);
		},
		remove(addedQuestion,i) {
			this.question_list.splice(i, 1);
			if (addedQuestion.dbsrc == "firebase"){
				this.firebase.push(addedQuestion)
			}
			
		},
		done() {
			this.$store.commit("addFinalQuestion", this.question_list); // what is this for?
			console.log("this.question_list :>> ", this.question_list);

			// invoke roomController/create
			window.location.href = `https://127.0.0.1:5000/create?pid=${this.userData.pid}&q=${JSON.stringify(this.question_list)}`;
			this.question_list = [];
		},
		
        getDataFromFirebase(){
            authAxios   
                .get("https://127.0.0.1:5000/getQuestionBank")
                .then((res) => {
					
                    this.firebase = Object.keys(res.data).map((question) => {
						return {
							title:res.data[question].title,
							choices: res.data[question].choices,
							dbsrc:res.data[question].dbsrc
						}
					});
					
                    console.log("firebase results", res.data)
                })
                .catch((err) => {
                    if (status == 400) {
                        console.log("Failed in fetching firebase db",err)
                    } 
                }) 
        },
	},

	computed: {
        ...mapState(['userData']),
		
	},

	created() {
		// redirect user if not logged in
		if (!this.userData) {
			// not logged in
			this.$router.push("/404_notLoggedIn")
		}
	},
};
</script>

<style>
b-button {
	padding: 20px;
}

#selfquestion {
	width: 560px;
}

@media screen and (max-width: 710px) {
	#selfquestion {
		width: 260px;
	}
}
</style>




/