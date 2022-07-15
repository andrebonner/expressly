<template>
  <article>
    <a-row>
      <a-col :style="{}">
        <div
          :style="{
            textAlign: 'center',
            margin: ' 0px auto',
            maxWidth: '500px',
          }"
        >
          <a-avatar :size="64" icon="check" />
          <h1>Thank you for the purchase!</h1>
          <p>You will receive an email confirmation shortly.</p>
          <a-button type="primary" @click="handleContineShopping" block>
            Continue Shopping
          </a-button>
        </div>
      </a-col>
    </a-row>
  </article>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Wholesale Checkout",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Wholesale Cart" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  methods: {
    handleContineShopping() {
      this.$router.push("/");
    },
  },
};
</script>
