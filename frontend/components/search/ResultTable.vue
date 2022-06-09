<template>
  <a-table
    :columns="columns"
    :row-key="(record) => record.id"
    :data-source="values.data"
    :pagination="{ pageSize: 10 }"
    :scroll="{ y: 240 }"
    v-show="values.data.length > 0"
  >
    <span slot="customTitle">{{
      values.type == "church" ? "Church" : "Institution"
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
const columns = [
  {
    dataIndex: "area",
    key: "area",
    title: "Area",
  },
  {
    dataIndex: "institution",
    key: "institution",
    slots: { title: "customTitle" },
  },
  {
    title: "Date/Time",
    key: "date",
    dataIndex: "date",
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
