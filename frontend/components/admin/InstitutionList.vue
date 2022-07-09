<template>
  <a-card title="Institutions" hoverable>
    <a-button
      slot="extra"
      type="primary"
      htmlType="button"
      @click="showInstModal()"
    >
      <a-icon type="plus"
    /></a-button>
    <a-list
      :loading="institutionLoading"
      item-layout="horizontal"
      :data-source="institutions"
      :pagination="pagination"
    >
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a slot="actions" @click="showInstModal(item)">Edit</a>
        <a-popconfirm
          title="Are you sure you want to delete this Institution?"
          ok-text="Yes"
          cancel-text="No"
          @confirm="confirmInstitutionDelete(item)"
          @cancel="cancelDelete"
          slot="actions"
          ><a href="#">Delete</a></a-popconfirm
        >
        <a-list-item-meta :description="item.name">
          <span slot="title">{{ item.code }}</span>
          <a-avatar slot="avatar" size="small" icon="build" />
        </a-list-item-meta>
        <div>{{ item.type }}</div>
      </a-list-item>
    </a-list>
    <a-modal
      v-model="institutionModal"
      :title="(institution.id ? 'Edit' : 'Create') + ' Institution'"
      on-ok="handleInstClick"
    >
      <a-form :form="institutionForm">
        <a-row :gutter="5">
          <a-col :span="12">
            <a-form-item label="Code">
              <a-input
                placeholder="Code"
                :disabled="institution.id > 0"
                v-decorator="[
                  'code',
                  {
                    initialValue: institution.code,
                    rules: [
                      { required: true, message: 'Please input code!' },
                      institution.id > 0
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
          </a-col>
          <a-col :span="12">
            <a-form-item label="Name">
              <a-input
                placeholder="Name"
                v-decorator="[
                  'name',
                  {
                    initialValue: institution.name,
                    rules: [{ required: true, message: 'Please input name!' }],
                  },
                ]"
                autocomplete="off"
              ></a-input> </a-form-item></a-col
        ></a-row>
        <a-row :gutter="5">
          <a-col :span="12">
            <a-form-item label="Type">
              <a-select
                placeholder="Type"
                v-decorator="[
                  'type',
                  {
                    initialValue: institution.type,
                    rules: [{ required: true, message: 'Please select type!' }],
                  },
                ]"
              >
                <a-select-option value="church">Church</a-select-option>
                <a-select-option value="space">Space</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="Telephone">
              <a-input
                placeholder="Telephone"
                v-decorator="[
                  'telephone',
                  {
                    initialValue: institution.telephone,
                    rules: [
                      { required: true, message: 'Please input telephone!' },
                    ],
                  },
                ]"
              ></a-input> </a-form-item></a-col
        ></a-row>
        <a-row :gutter="5">
          <a-form-item label="Email">
            <a-input
              placeholder="Email"
              v-decorator="[
                'email',
                {
                  initialValue: institution.email,
                  rules: [{ required: true, message: 'Please input email!' }],
                },
              ]"
            ></a-input>
          </a-form-item>
          <a-form-item label="Address">
            <a-textarea
              placeholder="Address"
              v-decorator="[
                'address',
                {
                  initialValue: institution.address,
                  rules: [{ required: true, message: 'Please input address!' }],
                },
              ]"
            ></a-textarea>
          </a-form-item>
        </a-row>
      </a-form>
      <template slot="footer">
        <a-button
          key="submit"
          type="primary"
          :loading="institutionLoading"
          @click="handleInstClick"
        >
          {{ institution.id ? "Update" : "Create" }}
        </a-button>
      </template>
    </a-modal>
  </a-card>
</template>
<script>
export default {
  data() {
    return {
      institutionModal: false,
      institution: {
        id: null,
        code: "",
        name: "",
        type: "",
        address: "",
        telephone: "",
        email: "",
      },
      institutionLoading: false,
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
    async getInstitutions() {
      this.institutionLoading = true;
      await this.$axios.get("/api/institutions").then((res) => {
        this.institutions = res.data;
        this.$store.commit("setInstitutions", this.institutions);
        this.institutionLoading = false;
      });
    },

    async createInstitution(form) {
      this.InstitutionLoading = true;
      await this.$axios.post("/api/institutions", form).then((res) => {
        if (res.data.success) {
          this.$message.success("Institution created successfully!");
          this.getInstitutions();
          this.institutionModal = false;
        } else {
          this.$message.error(res.data.message);
        }
        this.InstitutionLoading = false;
      });
    },
    async updateInstitution(form, code) {
      this.institutionLoading = true;
      await this.$axios.put("/api/institutions/" + code, form).then((res) => {
        if (res.data.success) {
          this.$message.success("Institution updated successfully!");
          this.getInstitutions();
          this.institutionModal = false;
        } else {
          this.$message.error(res.data.message);
        }
        this.institutionLoading = false;
      });
    },
    async deleteInstitution(record) {
      await this.$axios
        .delete("/api/institutions/" + record.code)
        .then((res) => {
          if (res.data.success) {
            this.$message.success("Deleted successfully!");
            this.getInstitutions();
          } else {
            this.$message.error(res.data.message);
          }
        });
    },

    showInstModal(record = null) {
      if (record) {
        this.institution = record;
        this.institutionForm.setFieldsValue({
          code: record.code,
          name: record.name,
          type: record.type,
          address: record.address,
          telephone: record.telephone,
          email: record.email,
        });
      } else {
        this.institution = {
          id: null,
          code: "",
          name: "",
          type: "",
          address: "",
          telephone: "",
          email: "",
        };
        this.institutionForm.resetFields();
      }
      this.institutionModal = true;
    },

    handleInstClick() {
      this.institutionForm.validateFields((err, values) => {
        if (!err) {
          console.log(values);
          if (this.institution.id) {
            this.updateInstitution(values, this.institution.code);
          } else {
            this.createInstitution(values);
          }
        }
      });
    },
    confirmInstitutionDelete(record) {
      this.deleteInstitution(record);
    },
    cancelDelete(e) {
      console.log(e);
      this.$message.info("Delete canceled");
    },
  },
  beforeCreate() {
    this.institutionForm = this.$form.createForm(this, {
      name: "institutionForm",
    });
  },
  mounted() {
    this.getInstitutions();
  },
};
</script>
