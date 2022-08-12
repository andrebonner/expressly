<template>
  <article>
    <a-row :gutter="8">
      <a-col :span="16">
        <a-card>
          <a-row :gutter="6">
            <a-col :span="8">
              <a-card hoverable>
                <img slot="cover" :alt="item.name" :src="item.photo.url" />
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
              :disabled="isAlreadyInCart()"
              @click="handleAddToCart"
              ><a-icon type="shopping-cart" />
              {{ isAlreadyInCart() ? "Added to cart" : "Add to cart" }}
            </a-button>
          </a-row></a-card
        ></a-col
      ><a-col :span="8">
        <a-card title="Ad Space"
          ><img
            src="https://unsplash.com/photos/LvySG1hvuzI/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjU3MzA5NzI1&force=true&w=640"
            alt="AD"
            :style="{ maxWidth: '100%' }"
        /></a-card> </a-col
    ></a-row>
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
  computed: {
    cart() {
      return this.$store.state.cart;
    },
  },
  data() {
    return {
      item: {
        name: "",
        price: "",
        category: {
          name: "",
        },
        description: "",
        photo: {
          url: "",
        },
      },
    };
  },
  methods: {
    async getItem(id) {
      const { data } = await this.$axios.get(`/api/items/${id}`);
      this.item = data;
    },
    async addToCart(item) {
      const { data } = await this.$axios
        .post(`/api/carts/item`, {
          item_id: item.id,
          quantity: 1,
        })
        .then((res) => {
          if (res.data.success) {
            const { cart } = res.data;
            this.$message.success("Item added to cart");
            this.$store.commit("setCart", cart);
          } else {
            this.$message.error(res.data.message);
          }
        });
    },
    handleAddToCart() {
      if (this.$auth.loggedIn) {
        this.$message.success("Added to cart");
        this.addToCart(this.item);
      } else {
        this.$message.error("You must be logged in to add to cart");
        this.$router.push({
          name: "login",
          query: { redirect: this.$route.fullPath },
        });
      }
    },
    isAlreadyInCart() {
      console.log(this.item, this.cart);
      return this.cart.items.find((i) => i.id == this.item.id);
    },
  },
  mounted() {
    this.getItem(this.$route.params.slug);
  },
};
</script>
