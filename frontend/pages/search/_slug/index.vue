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
    showTable(values) {
      console.log(this.activeKey, values);
      this.results = {
        type: this.activeKey,
        data: [
          {
            id: "1",
            area: "Kingston",
            institution: "Temple",
            date: "2020-01-01",
          },
          {
            id: "2",
            area: "Kingston",
            institution: "Unitarian",
            date: "2020-01-01",
          },
          {
            id: "3",
            area: "Kingston",
            institution: "Temple",
            date: "2020-01-01",
          },
          {
            id: "4",
            area: "Kingston",
            institution: "Unitarian",
            date: "2020-01-01",
          },
          {
            id: "5",
            area: "Kingston",
            institution: "Temple",
            date: "2020-01-01",
          },
          {
            id: "6",
            area: "Kingston",
            institution: "Unitarian",
            date: "2020-01-01",
          },
          {
            id: "7",
            area: "Kingston",
            institution: "Temple",
            date: "2020-01-01",
          },
          {
            id: "8",
            area: "Kingston",
            institution: "Unitarian",
            date: "2020-01-01",
          },
          {
            id: "9",
            area: "Kingston",
            institution: "Temple",
            date: "2020-01-01",
          },
          {
            id: "10",
            area: "Kingston",
            institution: "Unitarian",
            date: "2020-01-01",
          },
        ],
      };
      this.$nextTick(() => {
        this.$nuxt.$loading.start();
        setTimeout(() => {
          this.$nuxt.$loading.finish();
        }, 500);
      });
    },
  },
  mounted() {
    console.log(this.showResults);
    console.log("SearchPage mounted", this.$route.params.slug);
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
