<template>
  <article>
    <a-row :gutter="12">
      <a-col :span="16">
        <a-card>
          <a-list
            :pagination="pagination"
            :data-source="cart.items"
            :loading="loading"
          >
            <a-empty
              v-if="cart.items.length === 0"
              :image="require('~/assets/img/empty_cart.svg')"
              :image-style="{
                height: '300px',
              }"
            >
              <span slot="description">Cart is Empty </span>
            </a-empty>
            <a-list-item
              :key="item.id"
              slot="renderItem"
              slot-scope="item, index"
            >
              <img slot="extra" width="272" alt="logo" :src="item.photo.url" />
              <a-list-item-meta :description="item.description">
                <span slot="title">{{ item.name }}</span>
                <a-avatar slot="avatar" icon="shopping" />
              </a-list-item-meta>
              {{ item.content }}
            </a-list-item>
          </a-list>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card>
          <a-row :gutter="12" :style="{ marginBottom: '5px' }">
            <a-col :span="12">
              <a-card title="Total">
                <a-row :gutter="12">
                  <a-col :span="12">
                    <a-statistic :value="cart.total" :prefix="'$'" />
                  </a-col>
                </a-row>
              </a-card>
            </a-col>
            <a-col :span="12">
              <a-card title="Payment">
                <a-row :gutter="12">
                  <a-col :span="12">
                    <a-statistic :value="cart.total" :prefix="'$'" />
                  </a-col>
                </a-row>
              </a-card>
            </a-col> </a-row
          ><a-button
            type="primary"
            @click="handleCheckout"
            :disabled="cart.items.length === 0"
            block
            >Checkout</a-button
          >
        </a-card></a-col
      >
    </a-row>
  </article>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Wholesale Cart",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Wholesale Cart" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  data() {
    return {
      loading: false,
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0,
        onChange: (page) => {
          console.log(page);
          this.fetchCart();
        },
      },
      cart: {
        items: [],
        total: 0,
      },
    };
  },
  methods: {
    handleCheckout() {
      this.checkoutCart();
    },
    async fetchCart() {
      this.loading = true;
      await this.$axios.get("/api/cart").then((res) => {
        this.loading = false;
        this.cart = res.data;
        this.$store.commit("setCart", res.data);
      });
    },
    async checkoutCart() {
      await this.$axios.put("/api/cart/checkout").then((res) => {
        this.$message.success("Checkout Success");
        this.$store.commit("setCart", {
          items: [],
          total: 0,
        });
        this.$router.push("/cart/checkout");
      });
    },
  },
  mounted() {
    this.fetchCart();
  },
  middleware: ["auth"],
};
</script>
