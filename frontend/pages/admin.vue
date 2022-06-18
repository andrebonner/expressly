<template>
  <section>
    <a-row :gutter="6" :style="{ padding: '10px 0' }">
      <a-col :span="12">
        <a-card title="Areas" hoverable>
          <a-button
            slot="extra"
            type="primary"
            htmlType="button"
            @click="showAreaModal"
            ><a-icon type="plus"
          /></a-button>
          <a-list
            :loading="areaLoading"
            item-layout="horizontal"
            :data-source="areas"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a slot="actions" @click="showAreaModal(item)">edit</a>
              <a slot="actions">more</a>
              <a-list-item-meta :description="item.name">
                <span slot="title">{{ item.code }}</span>
                <a-avatar
                  slot="avatar"
                  src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                />
              </a-list-item-meta>
            </a-list-item>
          </a-list>
          <a-modal
            v-model="areaModal"
            title="Area Form"
            on-ok="handleAreaClick"
          >
            <a-form>
              <a-form-item label="Code">
                <a-input
                  v-model="area.code"
                  placeholder="Code"
                  :rules="[{ required: true, message: 'Please input code!' }]"
                ></a-input>
                <a-icon type="info-circle" />
              </a-form-item>
              <a-form-item label="Name">
                <a-input
                  v-model="area.name"
                  placeholder="Name"
                  :rules="[{ required: true, message: 'Please input name!' }]"
                ></a-input>
                <a-icon type="info-circle" />
              </a-form-item>
            </a-form>
            <template slot="footer">
              <a-button
                key="submit"
                type="primary"
                :loading="areaLoading"
                @click="handleAreaClick"
              >
                Submit
              </a-button>
            </template>
          </a-modal>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="Institutions" hoverable>
          <a-button slot="extra" type="primary" htmlType="button"
            ><a-icon type="plus"
          /></a-button>
          <a-list
            :loading="institutionLoading"
            item-layout="horizontal"
            :data-source="institutions"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a slot="actions">edit</a>
              <a slot="actions">more</a>
              <a-list-item-meta :description="item.name">
                <a slot="title" href="https://www.antdv.com/">{{
                  item.code
                }}</a>
                <a-avatar
                  slot="avatar"
                  src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                />
              </a-list-item-meta>
              <div>content</div>
            </a-list-item>
          </a-list>
        </a-card>
      </a-col> </a-row
    ><a-row :gutter="6" :style="{ padding: '10px 0' }">
      <a-col :span="12">
        <a-card title="Schedules" hoverable>
          <a-button slot="extra" type="primary" htmlType="button"
            ><a-icon type="plus"
          /></a-button>
          <a-list
            :loading="scheduleLoading"
            item-layout="horizontal"
            :data-source="schedules"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a slot="actions">edit</a>
              <a slot="actions">more</a>
              <a-list-item-meta
                :description="
                  item.institution.code + ' ' + item.institution.name
                "
              >
                <a slot="title" href="https://www.antdv.com/">{{
                  item.area.code + " " + item.area.name
                }}</a>
                <a-avatar
                  slot="avatar"
                  src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                />
              </a-list-item-meta>
              <div>content</div>
            </a-list-item>
          </a-list>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="Users" hoverable>
          <a-button slot="extra" type="primary" htmlType="button"
            ><a-icon type="plus"
          /></a-button>
          <a-list
            :loading="userLoading"
            item-layout="horizontal"
            :data-source="users"
            :pagination="pagination"
          >
            <a-list-item slot="renderItem" slot-scope="item, index">
              <a slot="actions">edit</a>
              <a slot="actions">more</a>
              <a-list-item-meta :description="item.email">
                <a slot="title" href="https://www.antdv.com/">{{
                  item.name
                }}</a>
                <a-avatar
                  slot="avatar"
                  src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                />
              </a-list-item-meta>
            </a-list-item>
          </a-list>
        </a-card>
      </a-col>
    </a-row>
  </section>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Admin",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Admin" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  data() {
    return {
      areaModal: false,
      area: {},
      areaLoading: false,
      institutionLoading: false,
      scheduleLoading: false,
      userLoading: false,
      areas: [],
      institutions: [],
      schedules: [],
      users: [],
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 3,
      },
    };
  },
  methods: {
    async getAreas() {
      this.areaLoading = true;
      await this.$axios.get("/api/areas").then((res) => {
        this.areas = res.data;
        this.areaLoading = false;
      });
    },
    async getInstitutions() {
      this.institutionLoading = true;
      await this.$axios.get("/api/institutions").then((res) => {
        this.institutions = res.data;
        this.institutionLoading = false;
      });
    },
    async getSchedules() {
      this.scheduleLoading = true;
      await this.$axios.get("/api/schedules").then((res) => {
        this.schedules = res.data;
        this.scheduleLoading = false;
      });
    },
    async getUsers() {
      this.userLoading = true;
      await this.$axios.get("/api/users").then((res) => {
        this.users = res.data;
        console.log(this.users);
        this.userLoading = false;
      });
    },
    showAreaModal(record = null) {
      if (record) this.area = record;
      this.areaModal = true;
    },
    handleAreaClick() {
      this.areaModal = false;
    },
  },
  mounted() {
    this.getAreas();
    this.getInstitutions();
    this.getSchedules();
    this.getUsers();
  },
  middleware: ["admin-auth"],
};
</script>
