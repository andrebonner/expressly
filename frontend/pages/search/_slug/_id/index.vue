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
          :title="
            capitalize(type) +
            ' Details ' +
            (schedule.date ? dateFormat(schedule.date) : '')
          "
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
      <p>
        This agreement is made between you
        {{ $auth.isloggedIn ? $auth.user.name : "" }} and {{ "Expressly" }}.
      </p>
      <p>
        The booking is for
        {{ schedule.institution ? schedule.institution.name : "" }} on the
        {{ schedule.date ? dateFormat(schedule.date) : "" }} at
        {{ schedule.time ? timeFormat(schedule.time) : "" }}.
      </p>
      <p>
        You may contact
        {{ schedule.institution ? schedule.institution.name : "" }} by phone
        {{ schedule.institution ? schedule.institution.telephone : "" }} or
        email {{ schedule.institution ? schedule.institution.email : "" }}
      </p>
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
      await this.$axios
        .get("/api/schedules/" + type + "/" + id)
        .then((response) => {
          this.schedule = response.data;
        });
    },
    openBookModal() {
      if (this.$auth.loggedIn) {
        this.visible = true;
      } else {
        this.$message.error("You must be logged in to book a slot");
        this.$router.push({
          path: "/login",
          query: {
            redirect: this.$route.fullPath,
          },
        });
      }
    },

    async handleClick(e) {
      try {
        this.loading = true;
        const result = await this.createBooking();

        if (result.success) {
          this.$message.success("Booking successful");
          this.visible = false;
          this.$router.push({
            path: "/bookings",
          });
        } else {
          this.$message.error(result.message);
        }
      } catch (error) {
        this.$message.error(error.message);
      } finally {
        this.loading = false;
      }
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
    async createBooking() {
      const response = await this.$axios.post("/api/bookings", {
        schedule_id: this.schedule.id,
        user_id: this.$auth.user.id,
      });

      return response.data;
    },
  },
  mounted() {
    console.log(this.$route.params);
    this.type = this.$route.params.slug;
    this.getDetails(this.type, this.$route.params.id);
  },
};
</script>
