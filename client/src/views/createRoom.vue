<template>
<div class="room">

    <h1> Hello, Kenny! </h1>
    <!-- do v-if roomID =='', show modal button. 
    Generae random roomID, add to roomID, show create Question page-->
    <div v-if="roomID.length < 0">
        <b-button variant="primary" v-b-modal.modal-1 @click="generateRoom()">Create New Room</b-button>

        <b-modal id="modal-1" title="This is your Room ID">
            <p class="my-4">{{roomID}}</p>
        </b-modal>
    </div>
    <div v-else>
        <!-- create question, and add question [] -->
    </div>
    
    
</div>
    
</template>

<script>
export default {
    name: 'room',
    data(){
        return{
            roomID:'',
            question: []
        }
    },
    methods: {
        generateRoom(){
            this.roomID = Math.random()*100;
        }
    }

}
    
    
        
    


</script>

<style>

</style>