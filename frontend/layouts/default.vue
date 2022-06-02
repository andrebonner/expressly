<template>
  <a-layout :style="{ minHeight: '100vh' }">
    <a-layout-header
      :style="{
        position: 'fixed',
        zIndex: 1,
        width: '100%',
      }"
    >
      <Navbar />
    </a-layout-header>
    <a-layout-content :style="{ padding: '0 50px', marginTop: '64px' }">
      <div :style="{ padding: '24px', minHeight: '380px' }">
        <nuxt />
      </div>
    </a-layout-content>
    <a-layout-footer :style="{ textAlign: 'center' }">
      Ant Design ©2018 Created by Ant UED
    </a-layout-footer>
  </a-layout>
</template>
<style>
.logo {
  width: 120px;
  height: 31px;
  /* background: rgba(255, 255, 255, 0.2); */
  margin: 16px 24px 16px 0;
  float: left;
}
.logo h2 {
  color: #fff;
  line-height: 31px;
}
</style>
