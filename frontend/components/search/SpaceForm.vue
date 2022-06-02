<template>
  <a-form
    layout="inline"
    :form="form"
    name="basic"
    autocomplete="off"
    @submit="handleSubmit"
  >
    <a-form-item name="select" has-feedback>
      <a-select
        v-decorator="[
          'area',
          {
            rules: [{ required: true, message: 'Please select your area!' }],
          },
        ]"
        :style="{ width: '100px' }"
        placeholder="Area"
      >
        <a-select-option value="china">China</a-select-option>
        <a-select-option value="usa">U.S.A</a-select-option>
      </a-select>
    </a-form-item>
    <a-form-item name="select" has-feedback>
      <a-select
        v-decorator="[
          'institution',
          {
            rules: [
              {
                required: true,
                message: 'Please select your institution!',
              },
            ],
          },
        ]"
        :style="{ width: '100px' }"
        placeholder="Institution"
      >
        <a-select-option value="mega-mart">Mega Mart</a-select-option>
        <a-select-option value="super-plus">Super +</a-select-option>
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
      <a-button type="primary" html-type="submit">Submit</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
export default {
  data() {
    return {
      activeKey: "church",
      areas: [
        { label: "Beijing", value: "Beijing" },
        { label: "Shanghai", value: "Shanghai" },
      ],
      form: this.$form.createForm(this),
    };
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      console.log(e);
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
        }
      });
    },
  },
};
</script>
