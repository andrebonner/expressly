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
                        initialValue: '1',
                        rules: [
                          { required: true, message: 'Please select category' },
                        ],
                      },
                    ]"
                  >
                    <a-select-option value="1">Category 1</a-select-option>
                    <a-select-option value="2">Category 2</a-select-option>
                    <a-select-option value="3">Category 3</a-select-option>
                  </a-select>
                </a-form-item>
              </a-form>
            </div>
            <a-list
              item-layout="vertical"
              size="large"
              :pagination="pagination"
              :data-source="items"
            >
              <a-list-item
                :key="item.id"
                slot="renderItem"
                slot-scope="item, index"
              >
                <template v-for="{ type, text } in actions" slot="actions">
                  <span :key="type" @click="handleAction(type)">
                    <a-icon :type="type" style="margin-right: 8px" />
                    {{ text }}
                  </span>
                </template>
                <img
                  slot="extra"
                  width="272"
                  alt="logo"
                  src="https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png"
                />
                <a-list-item-meta :description="item.description">
                  <a slot="title" :href="item.href">{{ item.title }}</a>
                  <a-avatar slot="avatar" :src="item.avatar" />
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
  data() {
    return {
      category: "1",
      items: [
        {
          href: "https://www.antdv.com/",
          title: `ant design vue part 1`,
          avatar:
            "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
          description:
            "Ant Design, a design language for background applications, is refined by Ant UED Team.",
          content:
            "We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.",
        },
        {
          href: "https://www.antdv.com/",
          title: `ant design vue part 2`,
          avatar:
            "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
          description:
            "Ant Design, a design language for background applications, is refined by Ant UED Team.",
          content:
            "We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.",
        },
        {
          href: "https://www.antdv.com/",
          title: `ant design vue part 3`,
          avatar:
            "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
          description:
            "Ant Design, a design language for background applications, is refined by Ant UED Team.",
          content:
            "We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.",
        },
      ],
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
    handleSearch(value) {
      this.$message.info(`Searching ${value}`);
      this.category = value;
    },
    handleAction(type) {
      switch (type) {
        case "eye":
          this.$message.info("View");
          this.$router.push("/wholesale/1/detail");
          break;
        case "shopping":
          if (this.$auth.loggedIn) {
            // TODO: add to cart
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
};
</script>
