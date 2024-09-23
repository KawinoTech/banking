<template>
    <div>
        <h>Cancel Operation</h>
        <button @click="$emit('close')">Cancel</button>
    </div>
</template>

<script>
    export default {
        name: 'Pop_Up',
        emits: ['close'],
        data() {
            return {
                data1: "Hello"
            }
        }
    }
    
</script>

<style lang="scss" scoped>
div {
    background-color: white;
}

</style>