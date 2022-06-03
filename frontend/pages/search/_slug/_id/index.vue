<template>
  <section>
    <a-row>
      <a-col :span="6">
        <a-card hoverable :style="{ width: '240px', padding: '4px' }">
          <img
            slot="cover"
            alt="example"
            src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
          />
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-descriptions :title="capitalize(type) + ' Details'">
          <a-descriptions-item label="UserName">
            Zhou Maomao
          </a-descriptions-item>
          <a-descriptions-item label="Telephone">
            1810000000
          </a-descriptions-item>
          <a-descriptions-item label="Live">
            Hangzhou, Zhejiang
          </a-descriptions-item>
          <a-descriptions-item label="Remark"> empty </a-descriptions-item>
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
