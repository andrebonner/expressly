<template>
  <a-card title="Areas" hoverable>
    <a-button
      slot="extra"
      type="primary"
      htmlType="button"
      @click="showAreaModal()"
      ><a-icon type="plus"
    /></a-button>
    <a-list
      :loading="areaLoading"
      item-layout="horizontal"
      :data-source="areas"
      :pagination="pagination"
    >
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a slot="actions" @click="showAreaModal(item)">Edit</a>
        <a-popconfirm
          title="Are you sure you want to delete this Area?"
          ok-text="Yes"
          cancel-text="No"
          @confirm="confirmAreaDelete(item)"
          @cancel="cancelDelete"
          slot="actions"
        >
          <a href="#">Delete</a></a-popconfirm
        >
        <a-list-item-meta :description="item.name">
          <span slot="title">{{ item.code }}</span>
          <a-avatar slot="avatar" size="small" icon="environment" />
        </a-list-item-meta>
      </a-list-item>
    </a-list>
    <a-modal
      v-model="areaModal"
      :title="(area.id ? 'Edit' : 'Create') + ' Area'"
      on-ok="handleAreaClick"
    >
      <a-form :form="areaForm">
        <a-form-item label="Code">
          <a-input
            placeholder="Code"
            :disabled="area.id > 0"
            v-decorator="[
              'code',
              {
                initialValue: area.code,
                rules: [
                  { required: true, message: 'Please input code!' },
                  {
                    pattern: /^[A-Z|a-z]{4}$/,
                    message: 'Please input valid code!',
                  },
                ],
              },
            ]"
          ></a-input>
        </a-form-item>
        <a-form-item label="Name">
          <a-input
            placeholder="Name"
            v-decorator="[
              'name',
              {
                initialValue: area.name,
                rules: [{ required: true, message: 'Please input name!' }],
              },
            ]"
            autocomplete="off"
          ></a-input>
        </a-form-item>
      </a-form>
      <template slot="footer">
        <a-button
          key="submit"
          type="primary"
          :loading="areaLoading"
          @click="handleAreaClick"
        >
          {{ area.id ? "Update" : "Create" }}
        </a-button>
      </template>
    </a-modal>
  </a-card>
</template>
<script>
export default {
  data() {
    return {
      areaModal: false,
      area: {
        id: null,
        code: "",
        name: "",
      },
      areaLoading: false,
      areas: [],
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

    async createArea(form) {
      this.areaLoading = true;
      await this.$axios.post("/api/areas", form).then((res) => {
        this.areaLoading = false;
        this.areaModal = false;
      });
    },
    async updateArea(form, id) {
      this.areaLoading = true;
      await this.$axios.put("/api/areas/" + id, form).then((res) => {
        this.areaLoading = false;
        this.areaModal = false;
      });
    },
    async deleteArea(record) {
      await this.$axios.delete("/api/areas/" + record.id).then((res) => {
        this.getAreas();
        this.$message({
          message: "Area Deleted!",
          type: "success",
        });
      });
    },

    showAreaModal(record = null) {
      this.areaModal = true;
      if (record) {
        this.area = record;
        this.areaForm.setFieldsValue({
          code: record.code,
          name: record.name,
        });
      } else {
        this.area = {
          id: null,
          code: "",
          name: "",
        };
        this.areaForm.resetFields();
      }
      console.log(record, this.area);
    },

    handleAreaClick() {
      this.areaForm.validateFields((err, values) => {
        if (!err) {
          console.log(values);
          if (this.area.id) {
            this.updateArea(values, this.area.id);
          } else {
            this.createArea(values);
          }
        }
      });
    },

    confirmAreaDelete(record) {
      this.deleteArea(record);
    },
    cancelDelete(e) {
      console.log(e);
      this.$message.info("Delete canceled");
    },
  },
  beforeCreate() {
    this.areaForm = this.$form.createForm(this, { name: "areaForm" });
  },
  mounted() {
    this.getAreas();
  },
};
</script>
