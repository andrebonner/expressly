<template>
  <nav>
    <div class="logo"><h2>Expressly</h2></div>
    <a-menu
      mode="horizontal"
      theme="dark"
      :style="{ lineHeight: '64px', float: 'right' }"
    >
      <a-menu-item key="1"
        ><router-link to="register">Register</router-link>
      </a-menu-item>
      <a-menu-item key="2"
        ><router-link to="login">Login</router-link>
      </a-menu-item>
    </a-menu>
  </nav>
</template>
