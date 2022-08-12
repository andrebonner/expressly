<template>
  <section>
    <a-row :gutter="6">
      <a-col :span="6">
        <a-card hoverable style="width: 240px">
          <img
            slot="cover"
            v-if="$auth.user.photo != undefined"
            alt="example"
            :src="$auth.user.photo.url"
          />
          <template slot="actions" class="ant-card-actions">
            <a-icon key="setting" type="setting" @click="handleSetting" />
            <a-icon key="edit" type="edit" @click="handleEdit" />
            <!-- <a-icon key="ellipsis" type="ellipsis" /> -->
          </template>
          <a-card-meta :title="$auth.user.name">
            <template slot="description">
              <p>
                <a-avatar size="small" icon="user" /> {{ $auth.user.email }}
              </p>
              <p v-if="$auth.user.account_type.name !== 'user'">
                {{ capitalize($auth.user.account_type.name) }}
                :
                {{ $auth.user.institution.name }}
              </p>
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
        <a-modal
          v-model="institutionModal"
          v-if="$auth.user.account_type.name !== 'user'"
          :title="
            $auth.user.institution.name +
            ' - ' +
            capitalize($auth.user.account_type.name)
          "
          on-ok="handleInstitutionSubmit"
        >
          <a-form layout="vertical" :form="institutionForm">
            <a-form-item label="Name">
              <a-input
                placeholder="Name"
                v-decorator="[
                  'name',
                  {
                    initialValue: $auth.user.institution.name,
                    rules: [{ required: true, message: 'Please input name!' }],
                  },
                ]"
              />
            </a-form-item>
            <a-form-item label="Address">
              <a-input
                placeholder="Address"
                v-decorator="[
                  'address',
                  {
                    initialValue: $auth.user.institution.address,
                    rules: [
                      { required: true, message: 'Please input address!' },
                    ],
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
                    initialValue: $auth.user.institution.email,
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
                    initialValue: $auth.user.institution.telephone,
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
            <a-button type="primary" @click="handleInstitutionSubmit"
              >Save</a-button
            >
          </template>
        </a-modal>
      </a-col>
      <a-col :span="18">
        <a-card
          title="Bookings"
          v-if="$auth.user.account_type.name == 'user'"
          style="width: 100%"
        >
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
        ><a-card
          title="Orders"
          v-if="$auth.user.account_type.name == 'user'"
          style="width: 100%"
        >
          <NuxtLink slot="extra" to="/orders" v-if="orders.length"
            >more</NuxtLink
          >
          <a-list
            item-layout="horizontal"
            :data-source="orders"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-list-item-meta :description="item.content">
                <a slot="title" @click="handleOrderClick(item)">{{
                  item.name
                }}</a>
                <a-avatar slot="avatar" size="small" icon="shopping-cart" />
              </a-list-item-meta>
            </a-list-item>
          </a-list>
        </a-card>
        <a-card
          title="Schedules"
          v-if="
            $auth.user.account_type.name == 'church' ||
            $auth.user.account_type.name == 'space'
          "
          style="width: 100%"
        >
          <NuxtLink
            slot="extra"
            to="/schedules"
            v-if="$auth.user.institution.schedules.length"
            >more</NuxtLink
          >
          <a-list
            item-layout="horizontal"
            :data-source="$auth.user.institution.schedules"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-list-item-meta
                :description="
                  item.area.name + ' - ' + $auth.user.institution.name
                "
              >
                <a slot="title" @click="handleScheduleClick(item)">{{
                  dateFormat(item.date) + " @ " + timeFormat(item.time)
                }}</a>
                <a-avatar slot="avatar" size="small" icon="calendar" />
              </a-list-item-meta>
            </a-list-item>
          </a-list>
        </a-card>
        <a-card
          title="Wholesale Items"
          v-if="$auth.user.account_type.name == 'wholesale'"
          style="width: 100%"
        >
          <NuxtLink slot="extra" to="/wholesale" v-if="items.length"
            >more</NuxtLink
          >
          <a-list
            item-layout="horizontal"
            :data-source="items"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a-list-item-meta :description="item.content">
                <a slot="title" @click="handleWholesaleClick(item)">{{
                  item.name
                }}</a>
                <a-avatar slot="avatar" size="small" icon="shopping-cart" />
              </a-list-item-meta>
            </a-list-item>
          </a-list>
        </a-card>
      </a-col>
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
      institutionModal: false,
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 3,
      },
      orders: [],

      items: [],
    };
  },
  beforeCreate() {
    this.profileForm = this.$form.createForm(this, {
      name: "profileForm",
      onFieldsChange(changedFields) {
        console.log(changedFields);
      },
    });
    this.institutionForm = this.$form.createForm(this, {
      name: "institutionForm",
      onFieldsChange(changedFields) {
        console.log(changedFields);
      },
    });
  },
  mounted() {
    console.log(this.$auth.user);
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
    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    },
    handleEdit(e) {
      this.profileModal = true;
    },
    handleSetting(e) {
      // change setting to account
      if (this.$auth.user.account_type.name === "user") {
        // switch to account types page
        this.$router.push("/upgrade");
      } else {
        // TODO: load modal based on account type

        if (
          this.$auth.user.account_type.name === "church" ||
          this.$auth.user.account_type.name === "space"
        ) {
          this.institutionModal = true;
        }
      }
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
    handleInstitutionSubmit(e) {
      console.log(e);
      this.institutionForm.validateFields((err, values) => {
        if (err) {
          return;
        }
        this.$axios
          .put("/api/institutions/" + this.$auth.user.institution.id, values)
          .then((res) => {
            if (res.data.success) {
              this.institutionModal = false;
              this.$message.info("Institution Updated");
            } else {
              this.$message.error(res.data.message);
            }
          });
      });
    },
  },
};
</script>
