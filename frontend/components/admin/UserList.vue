<template>
  <a-card title="Users" hoverable>
    <a-button
      slot="extra"
      type="primary"
      htmlType="button"
      @click="showUserModal"
    >
      <a-icon type="plus"
    /></a-button>
    <a-list
      :loading="userLoading"
      item-layout="horizontal"
      :data-source="users"
      :pagination="pagination"
    >
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a slot="actions" @click="showUserModal(item)">Edit</a>
        <a-popconfirm
          title="Are you sure you want to delete this User?"
          ok-text="Yes"
          cancel-text="No"
          @confirm="confirmUserDelete(item)"
          @cancel="cancelDelete"
          slot="actions"
          ><a href="#">Delete</a></a-popconfirm
        >
        <a-list-item-meta :description="item.email">
          <span slot="title">{{ item.name }}</span>
          <a-avatar slot="avatar" size="small" icon="user" />
        </a-list-item-meta>
      </a-list-item>
    </a-list>
    <a-modal
      v-model="userModal"
      :title="(user.id ? 'Edit' : 'Create') + ' User'"
      on-ok="handleUserClick"
    >
      <a-form :form="userForm">
        <a-form-item label="Name">
          <a-input
            placeholder="Name"
            v-decorator="[
              'name',
              {
                initialValue: user.name,
                rules: [{ required: true, message: 'Please input name!' }],
              },
            ]"
          ></a-input>
        </a-form-item>
        <a-form-item label="Email">
          <a-input
            placeholder="Email"
            v-decorator="[
              'email',
              {
                initialValue: user.email,
                rules: [{ required: true, message: 'Please input email!' }],
              },
            ]"
          ></a-input>
        </a-form-item>
        <a-form-item label="Telephone">
          <a-input
            placeholder="Telephone"
            v-decorator="[
              'telephone',
              {
                initialValue: user.telephone,
                rules: [{ required: true, message: 'Please input telephone!' }],
              },
            ]"
          ></a-input>
        </a-form-item>
      </a-form>
      <template slot="footer">
        <a-button
          key="submit"
          type="primary"
          :loading="userLoading"
          @click="handleUserClick"
        >
          {{ user.id ? "Update" : "Create" }}
        </a-button>
      </template>
    </a-modal>
  </a-card>
</template>
<script>
export default {
  data() {
    return {
      userModal: false,
      userLoading: false,
      user: {
        id: null,
        name: null,
        email: null,
        telephone: null,
      },
      users: [],
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 3,
      },
    };
  },
  methods: {
    async getUsers() {
      this.userLoading = true;
      await this.$axios.get("/api/users").then((res) => {
        this.users = res.data;
        this.userLoading = false;
      });
    },
    async createUser(form) {
      this.userLoading = true;
      await this.$axios.post("/api/users", form).then((res) => {
        this.userLoading = false;
        this.userModal = false;
      });
    },
    async updateUser(form, id) {
      this.userLoading = true;
      await this.$axios.put("/api/users/" + id, form).then((res) => {
        this.userLoading = false;
        this.userModal = false;
      });
    },
    async deleteUser(record) {
      await this.$axios.delete("/api/users/" + record.id).then((res) => {
        this.getUsers();
        this.$message({
          message: "User Deleted!",
          type: "success",
        });
      });
    },
    showUserModal(record = null) {
      if (record) {
        this.user = record;
        this.userForm.setFieldsValue(record);
      } else {
        this.user = {
          id: null,
          name: null,
          email: null,
          telephone: null,
        };
        this.userForm.resetFields();
      }
      this.userModal = true;
    },
    handleUserClick() {
      this.userForm.validateFields((err, values) => {
        if (!err) {
          console.log(values);
          if (this.user.id) {
            this.updateUser(values, this.user.id);
          } else {
            this.createUser(values);
          }
        }
      });
    },
    confirmUserDelete(record) {
      this.deleteUser(record);
    },
    cancelDelete(e) {
      console.log(e);
      this.$message.info("Delete canceled");
    },
  },
  beforeCreate() {
    this.userForm = this.$form.createForm(this, { name: "userForm" });
  },
  mounted() {
    this.getUsers();
  },
};
</script>
