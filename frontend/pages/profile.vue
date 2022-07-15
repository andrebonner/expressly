<template>
  <section>
    <a-row :gutter="12">
      <a-col :span="8">
        <a-card hoverable style="width: 240px">
          <img slot="cover" alt="example" :src="$auth.user.photo.url" />
          <template slot="actions" class="ant-card-actions">
            <a-icon key="setting" type="setting" @click="handleSetting" />
            <a-icon key="edit" type="edit" @click="handleEdit" />
            <!-- <a-icon key="ellipsis" type="ellipsis" /> -->
          </template>
          <a-card-meta :title="$auth.user.name">
            <template slot="description">
              <a-avatar size="small" icon="user" />
              {{ $auth.user.email }}
            </template>
          </a-card-meta>
        </a-card>
        <a-modal
          v-model="profileModal"
          :title="$auth.user.name + '\'s Profile'"
          on-ok="handleProfileSumbit"
        >
          <a-form layout="vertical" :form="profileForm">
            <a-form-item label="Name">
              <a-input
                placeholder="Name"
                v-decorator="[
                  'name',
                  {
                    initialValue: $auth.user.name,
                    rules: [{ required: true, message: 'Please input name!' }],
                  },
                ]"
              />
            </a-form-item>
            <a-form-item label="Email">
              <a-input
                placeholder="Email"
                v-decorator="[
                  'email',
                  {
                    initialValue: $auth.user.email,
                    rules: [
                      { required: true, message: 'Please input email!' },
                      { type: 'email', message: 'Please input valid email!' },
                    ],
                  },
                ]"
              />
            </a-form-item>
            <a-form-item label="Phone">
              <a-input
                placeholder="Phone"
                v-decorator="[
                  'telephone',
                  {
                    initialValue: $auth.user.telephone,
                    rules: [
                      { required: true, message: 'Please input phone!' },
                      {
                        pattern: /^1[3456789]\d{9}$/,
                        message: 'Please input valid phone!',
                      },
                    ],
                  },
                ]"
              />
            </a-form-item>
          </a-form>
          <template slot="footer">
            <a-button type="primary" @click="handleProfileSubmit"
              >Update</a-button
            >
          </template>
        </a-modal>
      </a-col>
      <a-col :span="12">
        <a-card title="Bookings" style="width: 100%">
          <NuxtLink
            slot="extra"
            to="/bookings"
            v-if="$auth.user.bookings.length"
            >more</NuxtLink
          >
          <a-list
            item-layout="horizontal"
            :data-source="$auth.user.bookings"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-list-item-meta
                :description="
                  item.schedule.area.name +
                  ' - ' +
                  item.schedule.institution.name
                "
              >
                <a slot="title" @click="handleBookingClick(item)">{{
                  dateFormat(item.schedule.date) +
                  " @ " +
                  timeFormat(item.schedule.time)
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
import moment from "moment";
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
      profileModal: false,
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 3,
      },
    };
  },
  beforeCreate() {
    this.profileForm = this.$form.createForm(this);
  },
  methods: {
    timeFormat(time) {
      let strTime, momTime;
      momTime = moment(time.split(".")[0], "HH:mm:ss");
      strTime = momTime.format("h:mm A");

      return strTime;
    },
    dateFormat(date) {
      let d = moment(date);

      return d.format("LL");
    },
    handleEdit(e) {
      this.profileModal = true;
    },
    handleSetting(e) {
      this.$message.info("Setting");
      // TODO: change setting to account
      // switch to account types page
    },
    handleBookingClick(item) {
      console.log(item);
      this.$message.info("Booking Click");
    },
    handleProfileSubmit(e) {
      console.log(e);
      this.profileForm.validateFields((err, values) => {
        if (err) {
          return;
        }
        this.$axios
          .put("/api/users/" + this.$auth.user.id, values)
          .then((res) => {
            if (res.data.success) {
              this.profileModal = false;
              this.$message.info("Profile Updated");
            } else {
              this.$message.error(res.data.message);
            }
          });
      });
    },
  },
};
</script>
