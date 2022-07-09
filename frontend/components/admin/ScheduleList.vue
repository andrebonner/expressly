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
          <a-col :span="8">
            <a-form-item label="Type">
              <a-select
                v-decorator="[
                  'type',
                  {
                    initialValue: schedule.type,
                    rules: [{ required: true, message: 'Please select type!' }],
                  },
                ]"
                @change="handleTypeChange"
                ><a-select-option value="church">Church</a-select-option>
                <a-select-option value="space">Space</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="Date">
              <a-date-picker
                format="YYYY-MM-DD"
                valueFormat="YYYY-MM-DD"
                v-decorator="[
                  'date',
                  {
                    initialValue: schedule.date,
                    rules: [{ required: true, message: 'Please select date!' }],
                  },
                ]"
              ></a-date-picker> </a-form-item
          ></a-col>
          <a-col :span="8">
            <a-form-item label="Time">
              <a-time-picker
                :use12-hours="true"
                format="h:mm A"
                valueFormat="HH:mm"
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
            <a-select-option
              v-for="institution in institutions"
              :key="institution.id"
            >
              {{ institution.code + " : " + institution.name }}
            </a-select-option>
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
            <a-select-option v-for="area in areas" :key="area.id">
              {{ area.code + " : " + area.name }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="Space Count">
          <a-input-number
            v-decorator="[
              'space_count',
              {
                initialValue: schedule.space_count,
                rules: [
                  { required: true, message: 'Please enter space count!' },
                ],
              },
            ]"
          ></a-input-number>
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
import moment from "moment";
export default {
  // computed: {
  //   institutions() {
  //     return this.$store.state.institutions;
  //   },
  //   areas() {
  //     return this.$store.state.areas;
  //   },
  // },
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
        type: null,
        space_count: 10,
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
    async createSchedule(form, type) {
      this.scheduleLoading = true;
      await this.$axios.post("/api/schedules/" + type, form).then((res) => {
        if (res.data.success) {
          this.$message.success("Schedule created successfully!");
          this.getSchedules();
          this.scheduleModal = false;
        } else {
          this.$message.error(res.data.message);
        }
        this.scheduleLoading = false;
      });
    },
    async updateSchedule(form, type, id) {
      this.scheduleLoading = true;
      await this.$axios
        .put("/api/schedules/" + type + "/" + id, form)
        .then((res) => {
          if (res.data.success) {
            this.$message.success("Schedule updated successfully!");
            this.getSchedules();
            this.scheduleModal = false;
          } else {
            this.$message.error(res.data.message);
          }
          this.scheduleLoading = false;
        });
    },
    async deleteSchedule(record) {
      console.log(record);
      await this.$axios
        .delete("/api/schedules/" + record.institution.type + "/" + record.id)
        .then((res) => {
          this.getSchedules();
          this.$message({
            message: "Schedule Deleted!",
            type: "success",
          });
        });
    },

    showScheduleModal(record = null) {
      if (record) {
        this.schedule = {
          id: record.id,
          area_id: record.area.id,
          institution_id: record.institution.id,
          date: this.dateFormat(record.date),
          time: this.timeFormat(record.time),
          type: record.institution.type,
          space_count: record.space_count,
        };
        this.scheduleForm.setFieldsValue({
          area_id: record.area.id,
          institution_id: record.institution.id,
          date: this.dateFormat(record.date),
          time: this.timeFormat(record.time),
          type: record.institution.type,
          space_count: record.space_count,
        });
        this.handleTypeChange(record.institution.type);
      } else {
        this.schedule = {
          id: null,
          area_id: null,
          institution_id: null,
          date: null,
          time: null,
          type: null,
          space_count: 10,
        };
        this.scheduleForm.resetFields();
      }
      console.log(this.schedule, record);
      this.scheduleModal = true;
    },
    handleScheduleClick() {
      this.scheduleForm.validateFields((err, values) => {
        if (!err) {
          console.log(values, this.schedule);
          if (this.schedule.id) {
            this.updateSchedule(values, values.type, this.schedule.id);
          } else {
            this.createSchedule(values, values.type);
          }
        }
      });
    },
    handleTypeChange(value) {
      const type = value;
      if (type) {
        this.areas = this.$store.state.areas.filter((area) => {
          return area.institutions[0]?.type == type;
        });
        this.institutions = this.$store.state.institutions.filter(
          (institution) => {
            return institution.type == type;
          }
        );
      }

      console.log(type, this.areas, this.institutions);
    },
    confirmScheduleDelete(record) {
      this.deleteSchedule(record);
    },
    cancelDelete(e) {
      console.log(e);
      this.$message.info("Delete canceled");
    },
    dateFormat(date) {
      return moment(date).format("YYYY-MM-DD");
    },
    timeFormat(time) {
      return moment(time.split(".")[0], "HH:mm:ss").format("HH:mm A");
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
