<template>
  <section>
    <Carousel />
    <a-tabs type="card" v-model:activeKey="activeKey">
      <a-tab-pane key="church" tab="Church">
        <h1>Book church attendance</h1>
        <ChurchForm />
      </a-tab-pane>
      <a-tab-pane key="space" tab="Space"
        ><h1>Book space in lin line</h1>
        <SpaceForm />
      </a-tab-pane>
    </a-tabs>
  </section>
</template>
<script>
import ChurchForm from "../../components/search/ChurchForm.vue";
import SpaceForm from "../../components/search/SpaceForm.vue";

export default {
  data() {
    return {
      activeKey: "church",
    };
  },
  methods: {},
  mounted() {
    console.log("SearchPage mounted", this.$route.params.slug);
    this.activeKey = this.$route.params.slug;
    this.$nextTick(() => {
      this.$nuxt.$loading.start();
      setTimeout(() => {
        this.$nuxt.$loading.finish();
      }, 500);
    });
  },
  components: { ChurchForm, SpaceForm },
};
</script>
