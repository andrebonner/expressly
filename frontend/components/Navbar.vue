<template>
  <nav>
    <div class="logo">
      <nuxt-link to="/"><h2>Expressly</h2></nuxt-link>
    </div>
    <a-menu
      v-if="!$auth.loggedIn"
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
    <a-menu
      v-if="$auth.loggedIn"
      mode="horizontal"
      theme="dark"
      :style="{ lineHeight: '64px', float: 'right' }"
    >
      <a-menu-item key="1" :title="$auth.user.name"
        ><nuxt-link to="/profile">Profile</nuxt-link>
      </a-menu-item>
      <a-menu-item key="2" @click="logout()">Logout </a-menu-item>
    </a-menu>
  </nav>
</template>
<script>
export default {
  methods: {
    async logout() {
      await this.$auth.logout();
      this.$message.success("Logged out successfully");
      this.$router.replace("/login");
    },
  },
};
</script>
