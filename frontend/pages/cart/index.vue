<template>
  <article>
    <a-row :gutter="12">
      <a-col :span="16">
        <a-card>
          <a-list :pagination="pagination" :data-source="cart.items">
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
              <img slot="extra" width="272" alt="logo" :src="item.image" />
              <a-list-item-meta :description="item.description">
                <a slot="title" :href="item.href">{{ item.name }}</a>
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
          ><a-button type="primary" @click="handleCheckout" block
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
      cart: {
        pagination: {
          page: 1,
          pageSize: 10,
          total: 0,
          onChange: (page, pageSize) => {
            this.fetchCart();
          },
        },
        items: [
          {
            id: "1",
            name: "Product 1",
            price: "100",
            quantity: "1",
            image:
              "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png",
          },
          {
            id: "2",
            name: "Product 2",
            price: "200",
            quantity: "2",
            image:
              "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png",
          },
          {
            id: "3",
            name: "Product 3",
            price: "300",
            quantity: "3",
            image:
              "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png",
          },
        ],
        total: 2000,
      },
    };
  },
  methods: {
    handleCheckout() {
      this.$message.success("Checkout Success");
      this.$router.push("/cart/checkout");
    },
    fetchCart() {
      this.cart.items = [
        {
          id: "1",
          name: "Product 1",
          price: "100",
          quantity: "1",
          image:
            "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png",
        },
        {
          id: "2",
          name: "Product 2",
          price: "200",
          quantity: "2",
          image:
            "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png",
        },
        {
          id: "3",
          name: "Product 3",
          price: "300",
          quantity: "3",
          image:
            "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png",
        },
      ];
      this.cart.total = 600;
    },
  },
};
</script>
