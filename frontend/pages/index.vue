<template>
  <Landing />
</template>

<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Welcome",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Welcome" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
};
</script>
