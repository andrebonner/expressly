<template>
  <section :style="{ margin: 'auto', width: '60%', padding: '10px' }">
    <a-row :gutter="12">
      <a-col :span="8">
        <h1 v-if="error.statusCode === 404">Page not found</h1>
        <h1 v-else-if="error.statusCode === 500">Internal Server error</h1>
        <h1 v-else>Something went wrong</h1>
        <p>{{ error.message }}</p>
        <p>{{ error.statusCode }}</p> </a-col
      ><a-col :span="8">
        <img
          v-if="error.statusCode === 404"
          src="~/assets/img/page_not_found.svg"
          width="300px"
          alt="error"
        />
        <img
          v-else-if="error.statusCode === 500"
          src="~/assets/img/server_down.svg"
          alt="error"
        />
        <img v-else src="~/assets/img/fixing_bugs.svg" alt="error" /> </a-col
    ></a-row>
    <a-row>
      <NuxtLink to="/">
        <a-button type="primary">Go to home</a-button>
      </NuxtLink></a-row
    >
  </section>
</template>
<script>
export default {
  props: ["error"],
  head() {
    return {
      templateTitle: "Error",
    };
  },
};
</script>
