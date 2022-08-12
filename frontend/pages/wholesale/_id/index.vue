<template>
  <article>
    <a-row :gutter="12">
      <a-col :span="16">
        <a-row :style="{ marginTop: '5px' }">
          <a-card title="Results">
            <div slot="extra" :style="{ minWidth: '200px' }">
              <a-form>
                <a-form-item>
                  <a-select
                    @change="handleSearch"
                    placeholder="Category"
                    v-decorator="[
                      'category',
                      {
                        initialValue: 1,
                        rules: [
                          { required: true, message: 'Please select category' },
                        ],
                      },
                    ]"
                  >
                    <a-select-option v-for="c in categories" :key="c.id">{{
                      c.name
                    }}</a-select-option>
                  </a-select>
                </a-form-item>
              </a-form>
            </div>
            <a-list
              item-layout="vertical"
              size="large"
              :pagination="pagination"
              :data-source="items"
              :loading="loading"
            >
              <a-list-item
                :key="item.id"
                slot="renderItem"
                slot-scope="item, index"
              >
                <template v-for="{ type, text } in actions" slot="actions">
                  <span :key="type" @click="handleAction(type, item)">
                    <a-icon :type="type" style="margin-right: 8px" />
                    {{ text }}
                  </span>
                </template>
                <img
                  slot="extra"
                  width="272"
                  alt="logo"
                  :src="item.photo.url"
                />
                <a-list-item-meta :description="item.description">
                  <a slot="title" :href="item.href">{{ item.name }}</a>
                  <a-avatar slot="avatar" icon="item" />
                </a-list-item-meta>
                {{ item.content }}
              </a-list-item>
            </a-list></a-card
          ></a-row
        >
      </a-col>
      <a-col :span="8">
        <a-card title="Ad space">
          <img
            src="https://unsplash.com/photos/LvySG1hvuzI/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjU3MzA5NzI1&force=true&w=640"
            alt="AD"
            :style="{ maxWidth: '100%' }"
          /> </a-card
      ></a-col>
    </a-row>
  </article>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Wholesale : Shop online then pay on pickup",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          hid: "description",
          name: "description",
          content: "Shop online pay on pickup",
        },
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
      loading: false,
      category: "1",
      items: [],
      categories: [],
      pagination: {
        pageSize: 10,
        current: 1,
      },
      actions: [
        {
          type: "eye",
          text: "View",
        },
        {
          type: "shopping",
          text: "Add to Cart",
        },
        {
          type: "credit-card",
          text: "Buy",
        },
      ],
    };
  },
  methods: {
    async getItems(wholesale_id) {
      this.loading = true;
      await this.$axios
        .get(`/api/wholesales/${wholesale_id}/items`)
        .then((res) => {
          this.loading = false;
          this.items = res.data;
          this.$store.commit("setItems", res.data);
        });
    },
    async getItemCategories() {
      const { data } = await this.$axios.get(`/api/items/categories`);
      this.categories = data;
    },
    async addToCart(item) {
      if (this.cart.items.find((i) => i.id === item.id)) {
        this.$message.error("Item is already in cart");
        return;
      }
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
    handleSearch(value) {
      this.$message.info(`Searching ...`);
      this.category = value;
      this.items = this.$store.state.items.filter(
        (item) => item.category.id === value
      );
    },
    handleAction(type, item) {
      switch (type) {
        case "eye":
          this.$router.push(`/wholesale/${item.wholesale_id}/${item.id}`);
          break;
        case "shopping":
          if (this.$auth.loggedIn) {
            this.addToCart(item);
          } else {
            this.$message.error("You must be logged in to add to cart");
            this.$router.push({
              name: "login",
              query: { redirect: this.$route.fullPath },
            });
          }
          break;
        case "credit-card":
          // TODO: buy now
          this.$message.info("Buy");
          break;
      }
    },
  },
  mounted() {
    const { id } = this.$route.params;
    this.getItems(id);
    this.getItemCategories();
  },
};
</script>
<style>
.ant-list-item-action {
  display: flex;
}
</style>
