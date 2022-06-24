<template>
  <section>
    <a-calendar
      :loading="loading"
      :disabled-date="disabledDate"
      @select="selectedDate"
    >
      <ul
        slot="dateCellRender"
        slot-scope="value"
        class="events"
        @click="handleDateClick(value)"
      >
        <li v-for="item in getListData(value)" :key="item.id">
          <a-badge :status="item.type" :text="item.content" />
        </li>
      </ul>
      <template slot="monthCellRender" slot-scope="value">
        <div
          v-if="getMonthData(value)"
          class="notes-month"
          @click="handleMonthClick(value)"
        >
          <section>{{ getMonthData(value) }}</section>
          <span>Event(s)</span>
        </div>
      </template>
    </a-calendar>
  </section>
</template>
<script>
import moment from "moment";
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
          const dt = moment(item.date);
          //console.log(dt.format("M/D/YYYY"), value.format("M/D/YYYY"));
          return dt.format("M/D/YYYY") === value.format("M/D/YYYY");
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
      const dt = moment();
      console.log(value.month(), dt.month());
      if (value.month() === dt.month()) {
        let monthData = this.bookings.filter((item) => {
          const dt2 = moment(item.date);
          console.log(dt2);
          return dt2.year() === value.year();
        });
        return monthData.length || 0;
      }
    },
    disabledDate(current) {
      return current < moment().startOf("day");
    },
    selectedDate(value) {
      console.log(value);
      this.$confirm({
        title: "Booking",
        content: "You have selected " + value.format("LL"),
        okText: "Book",
        cancelText: "Cancel",
        onOk() {
          console.log("OK");
          //this.$message.success("OK");
        },
        onCancel() {
          console.log("Cancel");
          //this.$message.error("Cancel");
        },
      });
    },
    handleDateClick(value) {
      console.log(value);
    },
    handleMonthClick(value) {
      console.log(value);
      this.$notification.info({
        message: "Booking",
        description: "You have selected " + value.format("MMMM"),
      });
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
