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
      ><a-menu-item key="1" v-if="$auth.user.is_admin"
        ><nuxt-link to="/admin">Admin</nuxt-link>
      </a-menu-item>
      <a-sub-menu>
        <template slot="title">
          <a-avatar size="small" icon="user" shape="square" />
          <span>{{ $auth.user.name }}</span>
        </template>
        <a-menu-item key="user-1"
          ><nuxt-link to="/profile">
            <a-icon type="user" />
            Profile</nuxt-link
          >
        </a-menu-item>
        <a-menu-item key="user-2"
          ><nuxt-link to="/cart"
            ><a-icon type="shopping-cart" />
            <a-badge
              v-if="cart.items.length > 0"
              :dot="true"
              :number-style="{ backgroundColor: '#52c41a' }"
            ></a-badge
            >&nbsp; Cart</nuxt-link
          >
        </a-menu-item>
        <a-menu-item key="user-3" @click="logout()">
          <a-icon type="logout" />
          Logout
        </a-menu-item>
      </a-sub-menu>
    </a-menu>
  </nav>
</template>
<script>
export default {
  computed: {
    cart() {
      console.log(this.$store.state.cart);
      return this.$store.state.cart;
    },
  },
  methods: {
    async logout() {
      await this.$auth.logout();
      this.$message.success("Logged out successfully");
      this.$router.replace("/login");
    },
  },
};
</script>
