<script setup></script>

<template>
  <div class="flex flex-row justify-between w-[1300px]">
    <router-link to="/">
      <div class="flex flex-row gap-3">
        <img class="cursor-not-allowed" src="/logo.png" alt="Logo" />
        <div class="gap-1 flex flex-col">
          <h1 class="text-xl font-bold uppercase font-mono font-italic cursor-pointer">
            Vue Subscribers
          </h1>
          <h2 class="cursor-help opacity-50 hover:opacity-100">
            Программа взаимных youtube подписок
          </h2>
        </div>
      </div>
    </router-link>
    <div>
      <ul class="flex flex-row justify-between w-[700px] gap-6">
        <router-link to="/signup">
          <li class="flex flex-row gap-2">
            <img class="w-15 h-10" src="/signup.png" alt="Signup" />
            <p class="text-2xl font-bold font-italic font-mono">Зарегистрироваться</p>
          </li>
        </router-link>
        <router-link to="/login">
          <li class="flex flex-row gap-2">
            <img class="w-10 h-10" src="/login.png" alt="Login" />
            <p class="text-2xl font-bold font-italic font-mono">Войти</p>
          </li>
        </router-link>
        <router-link to="/action">
          <li class="flex flex-row gap-2">
            <img class="w-10 h-10" src="/start.png" alt="Login" />
            <p class="text-2xl font-bold font-italic font-mono">Подписываться</p>
          </li>
        </router-link>
      </ul>
    </div>
  </div>
</template>
