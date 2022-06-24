<template>
  <a-card title="Schedules" hoverable>
    <a-button
      slot="extra"
      type="primary"
      htmlType="button"
      @click="showScheduleModal()"
    >
      <a-icon type="plus"
    /></a-button>
    <a-list
      :loading="scheduleLoading"
      item-layout="horizontal"
      :data-source="schedules"
      :pagination="pagination"
    >
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a slot="actions" @click="showScheduleModal(item)">Edit</a>
        <a-popconfirm
          title="Are you sure you want to delete this Schedule?"
          ok-text="Yes"
          cancel-text="No"
          @confirm="confirmScheduleDelete(item)"
          @cancel="cancelDelete"
          slot="actions"
          ><a href="#">Delete</a></a-popconfirm
        >
        <a-list-item-meta
          :description="item.institution.code + ' ' + item.institution.name"
        >
          <span slot="title">{{ item.area.code + " " + item.area.name }}</span>
          <a-avatar slot="avatar" size="small" icon="clock-circle" />
        </a-list-item-meta>
        <div>{{ item.date }}</div>
      </a-list-item>
    </a-list>
    <a-modal
      v-model="scheduleModal"
      :title="(schedule.id ? 'Edit' : 'Create') + ' Schedule'"
      on-ok="handleScheduleClick"
    >
      <a-form :form="scheduleForm"
        ><a-row :gutter="5">
          <a-col :span="12">
            <a-form-item label="Date">
              <a-date-picker
                v-decorator="[
                  'date',
                  {
                    initialValue: schedule.date,
                    rules: [{ required: true, message: 'Please select date!' }],
                  },
                ]"
              ></a-date-picker> </a-form-item
          ></a-col>
          <a-col :span="12">
            <a-form-item label="Time">
              <a-time-picker
                v-decorator="[
                  'time',
                  {
                    initialValue: schedule.time,
                    rules: [{ required: true, message: 'Please select time!' }],
                  },
                ]"
              ></a-time-picker>
            </a-form-item>
          </a-col> </a-row
        ><a-form-item label="Institution">
          <a-select
            v-decorator="[
              'institution_id',
              {
                initialValue: schedule.institution_id,
                rules: [
                  { required: true, message: 'Please select institution!' },
                ],
              },
            ]"
          >
            <a-option
              v-for="institution in institutions"
              :value="institution.id"
              :key="institution.id"
            >
              {{ institution.code + " " + institution.name }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item label="Area">
          <a-select
            v-decorator="[
              'area_id',
              {
                initialValue: schedule.area_id,
                rules: [{ required: true, message: 'Please select area!' }],
              },
            ]"
          >
            <a-option v-for="area in areas" :value="area.id" :key="area.id">
              {{ area.code + " " + area.name }}
            </a-option>
          </a-select>
        </a-form-item>
      </a-form>
      <template slot="footer">
        <a-button
          key="submit"
          type="primary"
          :loading="scheduleLoading"
          @click="handleScheduleClick"
        >
          {{ schedule.id ? "Update" : "Create" }}
        </a-button>
      </template>
    </a-modal>
  </a-card>
</template>
<script>
export default {
  data() {
    return {
      scheduleModal: false,
      scheduleLoading: false,
      schedule: {
        id: null,
        area_id: null,
        institution_id: null,
        date: null,
        time: null,
      },
      areas: [],
      institutions: [],
      schedules: [],
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 3,
      },
    };
  },
  methods: {
    async getSchedules() {
      this.scheduleLoading = true;
      await this.$axios.get("/api/schedules").then((res) => {
        this.schedules = res.data;
        this.scheduleLoading = false;
      });
    },
    async createSchedule(form) {
      this.scheduleLoading = true;
      await this.$axios.post("/api/schedules", form).then((res) => {
        this.scheduleLoading = false;
        this.scheduleModal = false;
      });
    },
    async updateSchedule(form, id) {
      this.scheduleLoading = true;
      await this.$axios.put("/api/schedules/" + id, form).then((res) => {
        this.scheduleLoading = false;
        this.scheduleModal = false;
      });
    },
    async deleteSchedule(record) {
      await this.$axios.delete("/api/schedules/" + record.id).then((res) => {
        this.getSchedules();
        this.$message({
          message: "Schedule Deleted!",
          type: "success",
        });
      });
    },

    showScheduleModal(record = null) {
      if (record) {
        this.schedule = record;
        this.scheduleForm.setFieldsValue(record);
      } else {
        this.schedule = {
          id: null,
          code: "",
          name: "",
          type: "",
          address: "",
          telephone: "",
          email: "",
        };
        this.scheduleForm.resetFields();
      }
      this.scheduleModal = true;
    },
    handleScheduleClick() {
      this.scheduleForm.validateFields((err, values) => {
        if (!err) {
          console.log(values);
          if (this.schedule.id) {
            this.updateSchedule(values, this.schedule.id);
          } else {
            this.createSchedule(values);
          }
        }
      });
    },
    confirmScheduleDelete(record) {
      this.deleteSchedule(record);
    },
    cancelDelete(e) {
      console.log(e);
      this.$message.info("Delete canceled");
    },
  },
  beforeCreate() {
    this.scheduleForm = this.$form.createForm(this, { name: "scheduleForm" });
  },
  mounted() {
    this.getSchedules();
  },
};
</script>
