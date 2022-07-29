<template>
  <section>
    <a-row :gutter="6">
      <a-col :span="18">
        <a-row :gutter="6">
          <a-col :span="6">
            <a-card hoverable :style="{ width: '240px', padding: '4px' }">
              <img
                slot="cover"
                :alt="capitalize(type)"
                :src="schedule.institution.photo.url"
              />
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card title="Booking Details">
              <div slot="extra" :style="{ minWidth: '200px' }">
                <a-button
                  type="primary"
                  :style="{ float: 'right' }"
                  @click="openBookModal"
                >
                  Book {{ schedule.time ? timeFormat(schedule.time) : "" }}
                  <a-icon type="right" />
                </a-button>
              </div>
              <a-descriptions
                :title="
                  capitalize(type) +
                  ' Details  - ' +
                  (schedule.date ? dateFormat(schedule.date) : '')
                "
              >
                <a-descriptions-item label="Name">
                  {{ schedule.institution ? schedule.institution.name : "" }}
                </a-descriptions-item>
                <a-descriptions-item label="Telephone">
                  {{
                    schedule.institution ? schedule.institution.telephone : ""
                  }}
                </a-descriptions-item>
                <a-descriptions-item label="Location">
                  {{ schedule.area ? schedule.area.name : "" }}
                </a-descriptions-item>

                <a-descriptions-item label="Address">
                  {{ schedule.institution ? schedule.institution.address : "" }}
                </a-descriptions-item>
              </a-descriptions></a-card
            ></a-col
          > </a-row
        ><a-row :gutter="8"> </a-row>
      </a-col>
      <a-col :span="6">
        <a-card title="Ad space">
          <img
            src="https://gw.alipayobjects.com/zos/rmsportal/nywPmnTAvTmLusPxHPSu.png"
            alt=""
          />
        </a-card> </a-col
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
import moment from "moment";
export default {
  head() {
    return {
      titleTemplate: "%s - Details",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Details" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  data() {
    return {
      type: "",
      visible: false,
      loading: false,
      schedule: {
        institution: {
          name: "",
          telephone: "",
          address: "",
          email: "",
          photo: {
            url: "",
          },
        },
        area: {
          name: "",
        },

        date: "",
        time: "",
      },
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
      let strTime = moment(time.split(".")[0], "HH:mm:ss").format("h:mm A");
      return strTime;
    },
    dateFormat(date) {
      let d = moment(date);

      return d.format("LL");
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
