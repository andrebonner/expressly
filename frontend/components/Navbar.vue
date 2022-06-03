<template>
  <nav>
    <div class="logo">
      <nuxt-link to="/"><h2>Expressly</h2></nuxt-link>
    </div>
    <a-menu
      mode="horizontal"
      theme="dark"
      :style="{ lineHeight: '64px', float: 'right' }"
    >
      <a-menu-item key="1"
        ><nuxt-link to="/register">Register</nuxt-link>
      </a-menu-item>
      <a-menu-item key="2"
        ><nuxt-link to="/login">Login</nuxt-link>
      </a-menu-item>
    </a-menu>
  </nav>
</template>
