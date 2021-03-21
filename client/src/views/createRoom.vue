<template>
<div class="room">
    <!-- do v-if="roomID.length < 0", show modal button. 
    Generae random roomID, add to roomID, show create Question page-->
    <div v-if="roomID.length <= 0">
        <b-button variant="dark" style="margin:50px; width:180px; height:50px;" @click="generateRoom()">Create New Room</b-button>
    </div>

    <div class="card" style="margin:20px auto; width:60%;" v-else>
        <div class="card-body">
            <h1>RoomID: {{roomID}}</h1>
            <b-button style="margin:20px;" variant="success" @click="createQuestion()">Create My Own Question</b-button>
            <b-button style="margin:20px;" variant="warning" @click="randomQuestion()">Generate Random Question</b-button>
            
            <!-- Random questions -->
            <div v-if="!createQ && randomQ">
                <ol>
                    <li style="text-align:left;" v-for="selfquestion in questions" :key="selfquestion">
                        <span><b>Question:</b> {{selfquestion.question}}</span><br>
                        <span><b>Choices:</b> {{selfquestion.choice}}</span><hr>
                    </li>
                
                </ol>
            </div>
            

            <!-- Create own question -->
            <div v-if="createQ && !randomQ">
                <b-form>
                <b-form-group id="input-group-1" label="Add New Question:" label-for="input-1">
                    <b-form-input id="input-1" v-model="newQ.question" placeholder="Enter your question." required></b-form-input>
                    <b-form-input id="input-1" v-model="newQ.choice1" placeholder="Enter choice 1" required></b-form-input>
                    <b-form-input id="input-1" v-model="newQ.choice2" placeholder="Enter choice 2" required></b-form-input>
                </b-form-group>

                <b-button variant="primary" @click="onSubmit">Submit</b-button>
                <b-button variant="danger" @click="onReset">Reset</b-button>
                </b-form>

                <b-card class="mt-3" header="Question">
                    <ol>
                        <li style="text-align:left;" v-for="question in selfQuestion" :key="question">
                            <span><b>Question:</b> {{question.question}}</span><br>
                            <span><b>Choices:</b> {{question.choice}}</span><hr>
                        </li>
                    </ol>
                </b-card>
            </div>

        </div>
    </div>
</div>
    
</template>

<script>
export default {
    // name: 'room',
    data: () => ({
        newQ:{
            question: "",
            choice1: "",
            choice2:""
        },
        randomQ: true,
        createQ: false
    }),
    methods: {
        generateRoom(){
            return this.$store.state.roomID = (Math.floor(Math.random()*1000000));
        },
        onSubmit(){
            this.$store.state.selfQuestion.push({
                question:this.newQ.question,
                choice:[this.newQ.choice1,this.newQ.choice2]
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
        randomQuestion(){
            this.randomQ = true;
            this.createQ = false;
        },
        createQuestion(){
            this.createQ = true;
            this.randomQ = false;
        }
    },
    
    computed:{
        roomID(){
            return this.$store.state.roomID;
        },
        questions(){
            return this.$store.state.questions;
        },
        selfQuestion(){
            return this.$store.state.selfQuestion;
        }
        
    }

}

</script>

<style>
b-button{
    padding:20px;
}
</style>




/