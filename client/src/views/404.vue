<template>
    <div>
        <h1>404 not found</h1>
        <p>To play a game, the URL should be <em>playGame/roomID.</em></p>
        <p>For now, only "testRoom" is available.</p>

    <div>
        <span
        @mouseover="hover = true"
        @mouseleave="hover = false"
        >
        Hover me to show the message!
        </span>
        <span v-if="hover">
            <br>
            <img id ="animation" src="../assets/animation.gif" />
        </span>
   </div>
    </div>
</template>
<script>
export default {
  data() {
    return {
      hover: false,
    };
  }
}
</script>