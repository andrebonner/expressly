<template>
  <article>
    <h1>{{ item.name }}</h1>
    <a-row :gutter="6">
      <a-col :span="8">
        <a-card hoverable>
          <img slot="cover" :alt="item.name" :src="item.image" />
        </a-card>
      </a-col>
      <a-col :span="16">
        <a-descriptions :title="item.name">
          <a-descriptions-item label="Name">{{
            item.name
          }}</a-descriptions-item>
          <a-descriptions-item label="Price">{{
            item.price
          }}</a-descriptions-item>
          <a-descriptions-item label="Category">{{
            item.category.name
          }}</a-descriptions-item>
          <a-descriptions-item label="Description">{{
            item.description
          }}</a-descriptions-item>
        </a-descriptions></a-col
      >
    </a-row>
    <a-row>
      <a-button
        type="primary"
        :style="{ float: 'right' }"
        @click="handleAddToCart"
        ><a-icon type="shopping-cart" /> Add to cart
      </a-button>
    </a-row>
  </article>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Wholesale Item",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Wholesale Item" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  data() {
    return {
      item: {
        id: 1,
        name: "Item 1",
        description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        price: 200,
        image:
          "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png",

        category: {
          id: 1,
          name: "Category 1",
          description: "This is category 1",
        },
      },
    };
  },
  methods: {
    handleAddToCart() {
      if (this.$auth.loggedIn) {
        this.$message.success("Added to cart");
        // TODO: add to cart
      } else {
        this.$message.error("You must be logged in to add to cart");
        this.$router.push({
          name: "login",
          query: { redirect: this.$route.fullPath },
        });
      }
    },
  },
};
</script>
