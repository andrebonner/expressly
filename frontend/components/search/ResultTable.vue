<template>
  <a-table
    :columns="columns"
    :row-key="(record) => record.id"
    :data-source="values.data"
    :pagination="{ pageSize: 10 }"
    :scroll="{ y: 240 }"
    v-show="values.data.length > 0"
  >
    <span slot="area" slot-scope="text, record">{{ record.area.name }}</span>
    <span slot="institution" slot-scope="text, record">{{
      record.institution.name
    }}</span>
    <span slot="date" slot-scope="text, record">{{
      values.type == "church"
        ? dateFormat(record.date)
        : dateFormat(record.date) + " : " + timeFormat(record.time)
    }}</span>
    <span slot="customIntsTitle">{{
      values.type == "church" ? "Church" : "Institution"
    }}</span>
    <span slot="customDateTimeTitle">{{
      values.type == "church" ? "Date" : "Date/Time"
    }}</span>
    <span slot="action" slot-scope="text, record">
      <a-button type="primary" @click="handleClick(record)">
        <a-icon type="info" />
        <span>Details</span>
      </a-button>
    </span>
  </a-table>
</template>
<script>
import moment from "moment";
const columns = [
  {
    dataIndex: "area",
    key: "area",
    title: "Area",
    scopedSlots: { customRender: "area" },
  },
  {
    dataIndex: "institution",
    key: "institution",
    slots: { title: "customIntsTitle" },
    scopedSlots: { customRender: "institution" },
  },
  {
    key: "date",
    dataIndex: "date",
    slots: { title: "customDateTimeTitle" },
    scopedSlots: { customRender: "date" },
  },
  {
    title: "Action",
    key: "action",
    scopedSlots: { customRender: "action" },
  },
];

export default {
  data() {
    return {
      columns,
      type: "",
    };
  },
  props: {
    values: {
      type: Object,
      default: {
        type: "",
        data: [],
      },
    },
  },
  methods: {
    dateFormat(date) {
      return moment(date).format("MMM DD, YYYY");
    },
    timeFormat(time) {
      return moment(time.split(".")[0], "HH:mm:ss").format("hh:mm A");
    },
    handleClick(row) {
      this.$router.push({
        path: this.values.type + "/" + row.id,
      });
      console.log(this.values.type);
    },
  },
  mounted() {},
};
</script>
