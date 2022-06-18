<template>
  <section>
    <a-row :gutter="12">
      <a-col :span="8">
        <a-card hoverable style="width: 240px">
          <img
            slot="cover"
            alt="example"
            src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
          />
          <template slot="actions" class="ant-card-actions">
            <a-icon key="setting" type="setting" />
            <a-icon key="edit" type="edit" @click="handleEdit" />
            <a-icon key="ellipsis" type="ellipsis" />
          </template>
          <a-card-meta :title="$auth.user.name">
            <template slot="description">
              <a-avatar size="small" icon="user" />
              {{ $auth.user.email }}
            </template>
          </a-card-meta>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="Bookings" style="width: 100%">
          <NuxtLink slot="extra" to="/bookings">more</NuxtLink>
          <a-list
            item-layout="horizontal"
            :data-source="$auth.user.bookings"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-list-item-meta
                :description="item.area.name + ' - ' + item.institution.name"
              >
                <a slot="title" @click="handleBookingClick(item)">{{
                  dateFormat(item.date) + " @ " + timeFormat(item.time)
                }}</a>
                <a-avatar slot="avatar" size="small" icon="calendar" />
              </a-list-item-meta>
            </a-list-item>
          </a-list> </a-card
      ></a-col>
    </a-row>
  </section>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Profile",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Landing Page" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  middleware: ["auth"],
  data() {
    return {
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 3,
      },
    };
  },
  methods: {
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
      // TODO: format date better
      let d = new Date(date);

      return d.toDateString();
    },
    handleEdit(e) {
      console.log(e);
      this.$message.info("User Edit");
    },
    handleBookingClick(item) {
      console.log(item);
      this.$message.info("Booking Click");
    },
  },
};
</script>
