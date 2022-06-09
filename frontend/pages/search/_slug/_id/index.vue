<template>
  <section>
    <a-row>
      <a-col :span="6">
        <a-card hoverable :style="{ width: '240px', padding: '4px' }">
          <img
            slot="cover"
            :alt="capitalize(type)"
            src="https://images.unsplash.com/photo-1564540574859-0dfb63985953?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=470&q=80"
          />
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-descriptions
          :title="capitalize(type) + ' Details ' + dateFormat(schedule.date)"
        >
          <a-descriptions-item label="Name">
            {{ schedule.institution ? schedule.institution.name : "" }}
          </a-descriptions-item>
          <a-descriptions-item label="Telephone">
            {{ schedule.institution ? schedule.institution.telephone : "" }}
          </a-descriptions-item>
          <a-descriptions-item label="Location">
            {{ schedule.area }}
          </a-descriptions-item>

          <a-descriptions-item label="Address">
            {{ schedule.institution ? schedule.institution.address : "" }}
          </a-descriptions-item>
        </a-descriptions></a-col
      > </a-row
    ><a-row
      ><a-button
        type="primary"
        :style="{ float: 'right' }"
        @click="openBookModal"
      >
        Book {{ schedule.time ? timeFormat(schedule.time) : "" }}
        <a-icon type="right" /> </a-button
    ></a-row>
    <a-modal
      v-model="visible"
      title="Information/Agreement"
      on-ok="handleClick"
    >
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
      schedule: {},
    };
  },
  props: {},
  methods: {
    async getDetails(type, id) {
      const response = await this.$axios.get(
        "/api/schedules/" + type + "/" + id
      );
      this.schedule = response.data;
    },
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
    timeFormat(time) {
      // TODO: format time better
      let hours = parseInt(time.split(":")[0]);
      let minutes = parseInt(time.split(":")[1]);
      let ampm = hours >= 12 ? " PM" : " AM";
      hours = hours % 12;
      let strTime = hours + ":" + minutes + ampm;
      return strTime;
    },
    dateFormat(date) {
      let d = new Date(date);
      let day = d.getDate(); // Day of the month without leading zeros
      let month = d.getMonth() + 1; // Month without leading zeros
      let year = d.getFullYear(); // Year
      let dateString = day + "/" + month + "/" + year;
      return dateString;
    },
  },
  mounted() {
    console.log(this.$route.params);
    this.type = this.$route.params.slug;
    this.getDetails(this.type, this.$route.params.id);
  },
};
</script>
