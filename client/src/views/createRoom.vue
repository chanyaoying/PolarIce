<template>
<div class="room">
    <!-- do v-if="roomID.length < 0", show modal button. 
    Generae random roomID, add to roomID, show create Question page-->
    <div v-if="!createdRoomID">
        <b-form>
            <h1 class="mt-5">Click the button to create New Room.</h1>
            <b-button variant="dark" style="margin:10px; width:180px; height:50px;" @click="generateRoom()">Create</b-button>
        </b-form>
    </div>

    <div class="card" style="margin:20px auto; width:90%;" v-else>
        <div class="card-body">
            <b-row>
                <b-col cols="10"> <h1>Room ID: {{roomID}}</h1> </b-col>
                <b-col><b-button variant="success" @click="done()">Done</b-button></b-col>
            </b-row>

            <b-container id="fluid">
                <b-row>
                    <b-col col="6">
                        <b-row>
                            <!-- create own question -->
                            <div>
                                <b-card class="mt-3" header="Create your own Question:" style="width:208%;">
                                    <b-form>
                                        <b-form-group id="input-group-1">
                                            <b-form-input v-model="newQ.question" placeholder="Enter your question." required></b-form-input>
                                            <b-form-input v-model="newQ.choice1" placeholder="Enter choice 1" required></b-form-input>
                                            <b-form-input v-model="newQ.choice2" placeholder="Enter choice 2" required></b-form-input>
                                        </b-form-group>

                                        <b-button variant="primary" @click="onSubmit" class="mr-4">Submit</b-button>
                                        <b-button variant="danger" @click="onReset">Reset</b-button>
                                    </b-form>
                                </b-card>
                            </div>
                        </b-row>

                        <b-row>
                            <!-- Random questions -->
                            <b-card class="mt-3" header="You can choose to use the following questions (optional):">
                                <div class="ml-4">
                                    <ol>
                                        <li style="text-align:left;" v-for="dbQuestion in questions" :key="dbQuestion">
                                            <b-row>
                                                <b-col cols="10">
                                                    <span><b>Question:</b> {{dbQuestion.question}}</span><br>
                                                    <span><b>Choices:</b> {{dbQuestion.choice}}</span>
                                                </b-col>
                                                <b-col>
                                                    <b-button variant="warning" @click="add(dbQuestion)">Add</b-button> 
                                                </b-col>
                                            </b-row>
                                            <hr>
                                        </li>  
                                    </ol>
                                </div>
                            </b-card>
                        </b-row>
                    </b-col>
                    <b-col col="6">
                        <b-card class="mt-3" header="Added Question">
                            <ol class="ml-3">
                                <li style="text-align:left;" v-for="addedQuestion in question_list" :key="addedQuestion">
                                    <b-row>
                                        <b-col cols="9">
                                            <span><b>Question:</b> {{addedQuestion.question}}</span><br>
                                            <span><b>Choices:</b> {{addedQuestion.choice}}</span>
                                        </b-col>
                                        <b-col>
                                            <b-button variant="danger" @click="remove(addedQuestion)">Remove</b-button> 
                                        </b-col>
                                    </b-row>
                                    <hr>
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
export default {
    // name: 'room',
    data: () => ({
        createdRoomID:false,
        roomID:'',
        userCreated:[],
        fireBase:[],
        final: [],
        question_list:[],
        newQ:{
            question: "",
            choice1: "",
            choice2:""
        }
    }),
    methods: {
        generateRoom(){
            this.roomID = (Math.floor(Math.random()*1000000));
            this.createdRoomID = true; 
        },
        onSubmit(){
            this.question_list.push({
                question:this.newQ.question,
                choice:[this.newQ.choice1,this.newQ.choice2],
                dbsrc:'user'
            });
            this.newQ.question = '';
            this.newQ.choice1 = '';
            this.newQ.choice2 = '';
        },
        onReset(){
            this.newQ.question = '';
            this.newQ.choice1 = '';
            this.newQ.choice2 = '';
        },
        add(dbQuestion){
            this.question_list.push(dbQuestion);
        },
        remove(addedQuestion){
            this.question_list.splice(addedQuestion, 1);
        },
        done(){
            for(var question in this.question_list)
                if (question.dbsrc == 'user'){
                    this.userCreated.push(question)
                }else if (question.dbsrc == 'firebase'){
                    this.fireBase.push(question)
                }
            this.final.push(
                {usercreated:this.userCreated, 
                firebase:this.fireBase,
                testBank:this.question_list
                }
            )

            this.$store.state.finalQuestion = this.final;
        }
    },
    
    computed:{
        questions(){
            return this.$store.getters.getFireBase;
        },
        // setNewRoomQuestions(finalQuestion){
        //     return this.$store.mutation.setNewRoomQuestions;
        // },

        
    }

}

</script>

<style>
b-button{
    padding:20px;
}
</style>




/