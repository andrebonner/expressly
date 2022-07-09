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
                  area.id > 0
                    ? {}
                    : {
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
          ></a-input> </a-form-item
        ><a-form-item label="Type" v-if="area.id > 0">
          <a-select
            v-decorator="[
              'type',
              {
                initialValue: area.type,
                rules: [{ required: false, message: 'Please select type!' }],
              },
            ]"
            @change="handleTypeChange"
            ><a-select-option value="church">Church</a-select-option>
            <a-select-option value="space">Space</a-select-option>
          </a-select> </a-form-item
        ><a-form-item label="Institution" v-if="area.id > 0">
          <a-select
            mode="multiple"
            v-decorator="[
              'institution_ids',
              {
                initialValue: area.institution_ids,
                rules: [
                  { required: false, message: 'Please select institution!' },
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
        type: "church",
        institution_ids: [],
      },
      areaLoading: false,
      areas: [],
      institutions: [],
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
        this.$store.commit("setAreas", this.areas);
        this.areaLoading = false;
      });
    },

    async createArea(form) {
      this.areaLoading = true;
      await this.$axios.post("/api/areas", form).then((res) => {
        if (res.data.success) {
          this.$message.success("Area created successfully!");
          this.getAreas();
          this.areaModal = false;
        } else {
          this.$message.error(res.data.message);
        }
        this.areaLoading = false;
      });
    },
    async updateArea(form, code) {
      this.areaLoading = true;
      await this.$axios.put("/api/areas/" + code, form).then((res) => {
        if (res.data.success) {
          this.$message.success("Area updated successfully!");
          this.getAreas();
          this.areaModal = false;
        } else {
          this.$message.error(res.data.message);
        }
        this.areaLoading = false;
      });
    },
    async deleteArea(record) {
      await this.$axios.delete("/api/areas/" + record.code).then((res) => {
        if (res.data.success) {
          this.$message.success("Area deleted successfully!");
          this.getAreas();
        } else {
          this.$message.error(res.data.message);
        }
      });
    },
    showAreaModal(record = null) {
      this.areaModal = true;
      if (record) {
        const type = this.getType(record);
        const inst_ids = record.institutions.map((inst) => {
          return inst.id;
        });
        console.log(inst_ids);
        this.area = {
          id: record.id,
          code: record.code,
          name: record.name,
          type: type,
          institution_ids: inst_ids,
        };
        this.areaForm.setFieldsValue({
          code: record.code,
          name: record.name,
          type: type,
          institution_ids: inst_ids,
        });
        this.handleTypeChange(type);
      } else {
        this.area = {
          id: null,
          code: "",
          name: "",
          type: "church",
          institution_ids: [],
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
            this.updateArea(values, this.area.code);
          } else {
            this.createArea(values);
          }
        }
      });
    },
    handleTypeChange(value) {
      const type = value;
      if (type) {
        this.institutions = this.$store.state.institutions.filter(
          (institution) => {
            return institution.type == type;
          }
        );
      }
    },
    confirmAreaDelete(record) {
      this.deleteArea(record);
    },
    cancelDelete(e) {
      console.log(e);
      this.$message.info("Delete canceled");
    },
    getType(record) {
      return record?.institutions ? record.institutions[0]?.type : "";
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
