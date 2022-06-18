<template>
  <section>
    <a-calendar :loading="loading">
      <ul slot="dateCellRender" slot-scope="value" class="events">
        <li v-for="item in getListData(value)" :key="item.id">
          <a-badge :status="item.type" :text="item.content" />
        </li>
      </ul>
      <template slot="monthCellRender" slot-scope="value">
        <div v-if="getMonthData(value)" class="notes-month">
          <section>{{ getMonthData(value) }}</section>
          <span>Backlog number</span>
        </div>
      </template>
    </a-calendar>
  </section>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Booking Calendar",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          hid: "description",
          name: "description",
          content: "Booking Calendar",
        },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  middleware: ["auth"],
  data() {
    return {
      visible: false,
      loading: false,
      bookings: [],
    };
  },
  mounted() {
    this.getBookings();
  },
  methods: {
    async getBookings() {
      this.loading = true;
      await this.$axios.get("/api/bookings").then((response) => {
        this.bookings = response.data;
        this.loading = false;
      });
    },
    getListData(value) {
      let listData, bookingData;
      if (value.date) {
        bookingData = this.bookings.filter((item) => {
          const dt = new Date(item.date);
          //console.log(dt.toLocaleDateString(), value.format("M/D/YYYY"));
          return dt.toLocaleDateString() === value.format("M/D/YYYY");
        });
        listData = bookingData.map((item) => {
          return {
            id: item.id,
            type: "success",
            content: `${item.institution.name} @ ${item.time}`,
          };
        });
        //console.log(listData);
      }

      return listData || [];
    },

    getMonthData(value) {
      const dt = new Date();
      console.log(value.month(), dt.getMonth() + 1);
      if (value.month() === dt.getMonth()) {
        let monthData = this.bookings.filter((item) => {
          const dt2 = new Date(item.date);
          console.log(dt2);
          return dt2.getFullYear() === value.year();
        });
        return monthData.length || 0;
      }
    },
  },
};
</script>
<style scoped>
.events {
  list-style: none;
  margin: 0;
  padding: 0;
}
.events .ant-badge-status {
  overflow: hidden;
  white-space: nowrap;
  width: 100%;
  text-overflow: ellipsis;
  font-size: 12px;
}
.notes-month {
  text-align: center;
  font-size: 28px;
}
.notes-month section {
  font-size: 28px;
}
</style>
