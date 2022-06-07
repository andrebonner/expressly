<template>
  <section>
    <a-row>
      <a-col :span="6">
        <a-card hoverable :style="{ width: '240px', padding: '4px' }">
          <img
            slot="cover"
            alt="example"
            src="https://images.unsplash.com/photo-1564540574859-0dfb63985953?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=470&q=80"
          />
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-descriptions :title="capitalize(type) + ' Details'">
          <a-descriptions-item label="Name">
            Abbley Church of God
          </a-descriptions-item>
          <a-descriptions-item label="Telephone">
            1810000000
          </a-descriptions-item>
          <a-descriptions-item label="Location">
            Hangzhou, Zhejiang
          </a-descriptions-item>

          <a-descriptions-item label="Address">
            No. 18, Wantang Road, Xihu District, Hangzhou, Zhejiang, China
          </a-descriptions-item>
        </a-descriptions></a-col
      > </a-row
    ><a-row
      ><a-button
        type="primary"
        :style="{ float: 'right' }"
        @click="openBookModal"
      >
        Book <a-icon type="right" /> </a-button
    ></a-row>
    <a-modal v-model="visible" title="Title" on-ok="handleClick">
      <template slot="footer">
        <a-button
          key="submit"
          type="primary"
          :loading="loading"
          @click="handleClick"
        >
          Complete Booking
        </a-button>
      </template>
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
    </a-modal>
  </section>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Details",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Landing Page" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  data() {
    return {
      type: "",
      visible: false,
      loading: false,
    };
  },
  props: {},
  methods: {
    openBookModal() {
      this.visible = true;
    },
    handleClick(row) {
      this.type = row.type;
      this.loading = true;
      setTimeout(() => {
        this.visible = false;
        this.loading = false;
      }, 3000);
    },
    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    },
  },
  mounted() {
    console.log(this.$route.params);
    this.type = this.$route.params.slug;
  },
};
</script>
