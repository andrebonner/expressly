<template>
  <a-form
    layout="inline"
    :form="form"
    name="basic"
    autocomplete="off"
    @submit.native.prevent="handleSubmit"
  >
    <a-form-item name="area" has-feedback>
      <a-select
        v-decorator="['area']"
        :style="{ width: '200px' }"
        placeholder="Area"
        :loading="areaLoading"
      >
        <a-select-option v-for="a in areas" :key="a.code">{{
          a.name
        }}</a-select-option>
      </a-select>
    </a-form-item>
    <a-form-item name="institution" has-feedback>
      <a-select
        v-decorator="['institution']"
        :style="{ width: '200px' }"
        placeholder="Church"
        :loading="institutionLoading"
      >
        <a-select-option v-for="c in churches" :key="c.code">{{
          c.name
        }}</a-select-option>
      </a-select>
    </a-form-item>
    <a-form-item name="date">
      <a-range-picker
        :disabled-date="disabledDate"
        v-decorator="[
          'date',
          {
            rules: [{ required: true, message: 'Please select date!' }],
          },
        ]"
        value-format="YYYY-MM-DD"
      /> </a-form-item
    ><a-form-item :wrapper-col="{ offset: 8, span: 16 }">
      <a-button type="primary" html-type="submit"
        ><a-icon type="search" />Search</a-button
      >
    </a-form-item>
  </a-form>
</template>
<script>
import moment from "moment";
export default {
  data() {
    return {
      activeKey: "church",
      areas: [],
      areaLoading: false,
      churches: [],
      institutionLoading: false,
      form: this.$form.createForm(this),
    };
  },
  methods: {
    async getAreas() {
      this.areaLoading = true;
      await this.$axios.get("/api/areas/church").then((res) => {
        this.areas = res.data;
        this.areaLoading = false;
      });
    },
    async getChurches() {
      this.institutionLoading = true;
      await this.$axios.get("/api/institutions/church").then((res) => {
        this.churches = res.data;
        this.institutionLoading = false;
      });
    },
    handleSubmit(e) {
      e.preventDefault();
      console.log(e);
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
          this.$emit("submitChurchSearch", values);
        }
      });
    },

    disabledDate(current) {
      // Can not select days before today
      return current < moment().startOf("day");
    },
  },
  mounted() {
    this.getAreas();
    this.getChurches();
  },
};
</script>
