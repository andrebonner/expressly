<template>
  <a-form
    layout="inline"
    :form="form"
    name="basic"
    autocomplete="off"
    @submit="handleSubmit"
  >
    <a-form-item name="area" has-feedback>
      <a-select
        v-decorator="['area']"
        :style="{ width: '200px' }"
        placeholder="Area"
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
        placeholder="Institution"
      >
        <a-select-option v-for="i in institutions" :key="i.code">{{
          i.name
        }}</a-select-option>
      </a-select>
    </a-form-item>
    <a-form-item
      name="date"
      :rules="[
        {
          type: 'string',
          required: true,
          message: 'Please select date!',
        },
      ]"
    >
      <a-date-picker
        v-decorator="[
          'date',
          {
            rules: [
              {
                type: 'string',
                required: true,
                message: 'Please select date!',
              },
            ],
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
export default {
  data() {
    return {
      activeKey: "church",
      areas: [],
      institutions: [],
      form: this.$form.createForm(this),
    };
  },
  mounted() {
    this.getAreas();
    this.getInstitutions();
  },
  methods: {
    async getAreas() {
      const response = await this.$axios.get("/api/areas/space");
      this.areas = response.data;
    },
    async getInstitutions() {
      const response = await this.$axios.get("/api/institutions/space");
      this.institutions = response.data;
    },

    handleSubmit(e) {
      e.preventDefault();
      console.log(e);
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
          this.$emit("submitSpaceSearch", values);
        }
      });
    },
  },
};
</script>
