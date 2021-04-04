<template>
	<div class="room">
		<!-- do v-if="roomID.length < 0", show modal button. 
    Generae random roomID, add to roomID, show create Question page-->
		<!-- <div v-if="!createdRoomID">
        <b-form>
            <h1 class="mt-5">Click the button to create New Room.</h1>
            <b-button variant="dark" style="margin:10px; width:180px; height:50px;" @click="generateRoom()">Create</b-button>
            <b-button variant="dark" style="margin:10px; width:180px; height:50px;" @click="getDataFromFirebase()">Get firebase data</b-button>
        </b-form>
    </div> -->

		<div class="card" style="margin: 20px auto; width: 90%">
			<div class="card-body">
				<b-row>
					<!-- <b-col cols="10"> <h1>Room ID: {{roomID}}</h1> </b-col> -->
					<b-col
						><b-button variant="success" @click="done()"
							>Done</b-button
						></b-col
					>
				</b-row>

				<b-container id="fluid">
					<b-row>
						<b-col col="6">
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
									header="You can choose to use the following questions (optional):"
								>
                                <button @click="getDataFromFirebase()">click me</button>
									<div class="ml-4">
										<ol>
											<li
												style="text-align: left"
												v-for="(
													dbQuestion, i
												) in firebase"
												:key="i"
											>
												<b-row>
													<b-col cols="10">
														<span
															><b>Question:</b>
															{{
																dbQuestion.title
															}}</span
														><br />
														<span
															><b>Choices:</b>
															{{
																dbQuestion.choices
															}}</span
														>
													</b-col>
													<b-col>
														<b-button
															variant="warning"
															@click="
																add(dbQuestion)
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
						<b-col col="6">
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
														remove(addedQuestion)
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
import sampleQuestion from "../store/sampleQuestions";
import { mapState } from 'vuex';

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
	methods: {
		// generateRoom(){
		//     this.roomID = (Math.floor(Math.random()*1000000));
		//     this.createdRoomID = true;
		// },
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
		add(dbQuestion) {
			this.question_list.push(dbQuestion);
		},
		remove(addedQuestion) {
			this.question_list.splice(addedQuestion, 1);
		},
		done() {
			this.$store.commit("addFinalQuestion", this.question_list); // what is this for?
			console.log("this.question_list :>> ", this.question_list);
			this.question_list = [];

			
            
            // temp
			let questions = sampleQuestion[0];

			// invoke roomManagement/create
			authAxios.get("https://127.0.0.1:5000/create", {
                pid: this.userData.pid,
                questions: questions,
            }).then((res) => {
				// send question info
                console.log('res :>> ', res);
			});
		},
        getDataFromFirebase(){
            authAxios   
                .get("https://127.0.0.1:5000/getQuestionBank")
                .then((res) => {
                    this.firebase.push(res.data) 
                    console.log("firebase results", res.data)
                })
                .catch((err) => {
                    if (status == 400) {
                        console.log("Failed in fetching firebase db",err)
                    } 
                }) 
            // return this.firebase;
        }
	},

	computed: {
        ...mapState(['userData']),
		questions() {
			return this.$store.getters.GetFireBase;
		},
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