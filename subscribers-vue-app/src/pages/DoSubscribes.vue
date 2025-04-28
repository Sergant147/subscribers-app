<template>
  <div>
    <h1>Youtube Channel Checker</h1>
    <button @click="openYouTubePage">Go to YouTube Channel</button>
    <div v-if="status">{{ status }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import html2canvas from 'html2canvas'

let youtubeWindow = null;
const status = ref('');

const openYouTubePage = () => {
  youtubeWindow = window.open("https://www.youtube.com/@fakng-engineer/", "_blank", "width=800,height=600");
  setTimeout(captureScreenshot, 5000); // wait 5 seconds for page to load
};

const captureScreenshot = async () => {
  if (!youtubeWindow) return;

  try {
    const canvas = await html2canvas(youtubeWindow.document.body);
    const imageData = canvas.toDataURL("image/png");

    const formData = new FormData();
    formData.append('file', dataURLtoBlob(imageData), 'screenshot.png');

    const response = await axios.post('http://localhost:8000/upload-screenshot', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.found) {
      status.value = '✅ Subscribed detected!';
    } else {
      status.value = '❌ Not subscribed.';
    }

    youtubeWindow.close();
  } catch (error) {
    console.error(error);
    status.value = '❌ Error occurred.';
  }
};

const dataURLtoBlob = (dataurl) => {
  const arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
    bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
  for (let i = 0; i < n; i++) {
    u8arr[i] = bstr.charCodeAt(i);
  }
  return new Blob([u8arr], { type: mime });
};
</script>

<style scoped>
button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
}
</style>
