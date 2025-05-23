<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-300 px-4"
  >
    <div class="bg-white shadow-xl rounded-xl p-8 max-w-md w-full space-y-6 text-center">
      <h2 class="text-3xl font-bold text-gray-800">Welcome</h2>
      <p class="text-gray-500">Choose a method to sign up</p>

      <!-- Google Sign-In Button -->
      <button
        @click="loginGoogle"
        class="w-full flex items-center justify-center gap-3 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 rounded-lg transition duration-300"
      >
        <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
          <path
            fill="#4285F4"
            d="M21.35 11.1H12v2.83h5.55c-.24 1.32-.96 2.43-2.04 3.18l3.3 2.57c1.94-1.79 3.06-4.43 3.06-7.58 0-.58-.05-1.15-.13-1.7z"
          />
          <path
            fill="#34A853"
            d="M12 22c2.7 0 4.97-.9 6.63-2.43l-3.3-2.57c-.92.61-2.1.97-3.33.97-2.56 0-4.72-1.73-5.5-4.06H3.1v2.56C4.8 19.92 8.16 22 12 22z"
          />
          <path
            fill="#FBBC05"
            d="M6.5 13.91A5.994 5.994 0 0 1 6 12c0-.66.11-1.3.31-1.91V7.53H3.1A9.997 9.997 0 0 0 2 12c0 1.57.37 3.05 1.03 4.47l3.47-2.56z"
          />
          <path
            fill="#EA4335"
            d="M12 6c1.47 0 2.8.51 3.84 1.5l2.88-2.88C17.01 2.7 14.7 2 12 2 8.16 2 4.8 4.08 3.1 7.53l3.47 2.56C7.28 7.73 9.44 6 12 6z"
          />
        </svg>
        Sign in with Google
      </button>

      <div class="relative">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-300"></div>
        </div>
        <div class="relative flex justify-center text-sm text-gray-500">
          <span class="bg-white px-2">Or continue with email</span>
        </div>
      </div>

      <!-- Manual Signup Form -->
      <form @submit.prevent="handleSubmit" class="space-y-4 text-left">
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Username</label>
          <input
            v-model="form.username"
            type="text"
            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Youtube URL</label>
          <input
            v-model="form.url"
            type="text"
            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">Password</label>
          <input
            v-model="form.password"
            type="password"
            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-md transition"
        >
          Sign up
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth'
import axios from 'axios'

// Firebase config
const firebaseConfig = {
  apiKey: 'AIzaSyD7QE6e627pF9XkNcDxQFONfsNM9tUITec',
  authDomain: 'project-29f84.firebaseapp.com',
  projectId: 'project-29f84',
  storageBucket: 'project-29f84.firebasestorage.app',
  messagingSenderId: '649551902433',
  appId: '1:649551902433:web:77800b39c3162a536da9a0',
  measurementId: 'G-0DLHM12P19',
}

const app = initializeApp(firebaseConfig)
const auth = getAuth(app)
auth.languageCode = 'en'
const provider = new GoogleAuthProvider()

function loginGoogle() {
  signInWithPopup(auth, provider)
    .then((result) => {
      const user = result.user
      console.log('Google user:', user)
      axios.post('http://localhost:8000/create_jwt-token/' + user)
      window.location.href = '/urlset'
    })
    .catch((error) => {
      console.error('Google Sign-In Error:', error.message)
    })
}

// Manual form state
const form = reactive({
  username: '',
  email: '',
  password: '',
  url: '',
})

function useAxiosToSendData(payload) {
  const path = 'http://127.0.0.1:8000/signup'
  const sitePayload = {
    username: payload.username,
    email: payload.email,
    password: payload.password,
    url: payload.url,
  }
  axios.post(path, sitePayload)
}

function handleSubmit() {
  useAxiosToSendData({
    username: form.username,
    email: form.email,
    password: form.password,
    url: form.url,
  })
}
</script>
