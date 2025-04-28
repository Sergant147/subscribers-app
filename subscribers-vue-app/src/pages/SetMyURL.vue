<script setup>
import axios from 'axios'
import { ref } from 'vue'
const url = ref('')
const sendData = () => {
  axios.post(`http://127.0.0.1:8000/create_jwt-token/${url.value}`)
  window.location.href = '/logged'
}
</script>

<template>
  <div class="mb-3">
    <label class="text-3xl font-bold">Your Youtube URL: </label>
    <input
      v-model="url"
      class="h-[50px] text-3xl font-bold italic border-3 rounded-xl border-red-400 p-2"
    />
  </div>
  <button
    @click="sendData"
    class="bg-blue-400 cursor-pointer hover:bg-blue-500 active:bg-blue-700 text-3xl p-4 rounded-2xl w-[400px] flex justify-center"
  >
    Submit URL
  </button>
</template>

<style scoped></style>
