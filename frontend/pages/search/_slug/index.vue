<template>
  <section>
    <Carousel />
    <a-tabs type="card" v-model:activeKey="activeKey">
      <a-tab-pane key="church" tab="Church">
        <h1>Book church attendance</h1>
        <ChurchForm @submitChurchSearch="showTable" />
      </a-tab-pane>
      <a-tab-pane key="space" tab="Space"
        ><h1>Book space in lin line</h1>
        <SpaceForm @submitSpaceSearch="showTable" />
      </a-tab-pane>
    </a-tabs>
    <ResultTable :values="results" />
  </section>
</template>
<script>
import ChurchForm from "~/components/search/ChurchForm.vue";
import SpaceForm from "~/components/search/SpaceForm.vue";
import ResultTable from "~/components/search/ResultTable.vue";

export default {
  head() {
    return {
      titleTemplate: "%s - Search",
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
      activeKey: "church",
      results: {
        type: "",
        data: [],
      },
    };
  },

  methods: {
    async search(type, params) {
      await this.$axios
        .get("/api/schedules?type=" + type, {
          params,
        })
        .then((response) => {
          this.results.type = type;
          this.results.data = response.data;
        });
    },
    showTable(values) {
      this.$nextTick(() => {
        this.$nuxt.$loading.start();
        this.search(this.activeKey, values);
        setTimeout(() => {
          this.$nuxt.$loading.finish();
        }, 500);
      });
    },
  },
  mounted() {
    console.log(this.showResults);
    console.log("SearchPage mounted", this.$route.query);
    this.activeKey = this.$route.params.slug;
  },
  components: { ChurchForm, SpaceForm, ResultTable },
};
</script>
<style>
.ant-tabs-card > .ant-tabs-content {
  height: 120px;
  margin-top: -16px;
}

.ant-tabs-card > .ant-tabs-content > .ant-tabs-tabpane {
  background: #fff;
  padding: 16px;
}

.ant-tabs-card > .ant-tabs-bar {
  border-color: #fff;
}

.ant-tabs-card > .ant-tabs-bar .ant-tabs-tab {
  border-color: transparent;
  background: transparent;
}

.ant-tabs-card > .ant-tabs-bar .ant-tabs-tab-active {
  border-color: #fff;
  background: #fff;
}
</style>
