<template>
  <section>
    <a-card :style="{ width: '450px', margin: ' 10px auto', padding: '10px' }">
      <a-form
        id="expressly-reset-password"
        :form="form"
        class="reset-password-form"
        @submit="handleSubmit"
      >
        <a-form-item>
          <a-input
            :disabled="user.id ? true : false"
            v-decorator="[
              'email',
              {
                initialValue: user.email,
                rules: [
                  {
                    type: 'email',
                    message: 'The input is not valid E-mail!',
                  },
                  { required: true, message: 'Please input your email!' },
                ],
              },
            ]"
            placeholder="Email"
          >
            <a-icon
              slot="prefix"
              type="mail"
              style="color: rgba(0, 0, 0, 0.25)"
            />
          </a-input>
        </a-form-item>
        <a-form-item has-feedback>
          <a-input
            v-decorator="[
              'password',
              {
                rules: [
                  { required: true, message: 'Please input your Password!' },
                  {
                    validator: validateToNextPassword,
                  },
                ],
              },
            ]"
            type="password"
            placeholder="Password"
          >
            <a-icon
              slot="prefix"
              type="lock"
              style="color: rgba(0, 0, 0, 0.25)"
            />
          </a-input>
        </a-form-item>
        <a-form-item has-feedback>
          <a-input
            v-decorator="[
              'confirmpassword',
              {
                rules: [
                  {
                    required: true,
                    message: 'Please input your confirm Password!',
                  },
                  {
                    validator: compareToFirstPassword,
                  },
                ],
              },
            ]"
            type="password"
            @blur="handleConfirmBlur"
            placeholder="Confirm Password"
          >
            <a-icon
              slot="prefix"
              type="lock"
              style="color: rgba(0, 0, 0, 0.25)"
            />
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            class="reset-password-form-button"
            :loading="loading"
          >
            Reset Password
          </a-button>
        </a-form-item>
      </a-form></a-card
    >
  </section>
</template>
<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Reset Password",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Reset Password" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  data() {
    return { loading: false, user: {} };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "normal_reset_password" });
  },
  mounted() {
    this.getUser();
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
          this.resetPassword(values);
        }
        console.log(err);
      });
    },
    handleConfirmBlur(e) {
      const value = e.target.value;
      this.confirmDirty = this.confirmDirty || !!value;
    },
    compareToFirstPassword(rule, value, callback) {
      const form = this.form;
      if (value && value !== form.getFieldValue("password")) {
        callback(new Error("Two passwords that you enter is inconsistent!"));
      } else {
        callback();
      }
    },
    validateToNextPassword(rule, value, callback) {
      const form = this.form;
      if (value && this.confirmDirty) {
        form.validateFields(["confirmpassword"], { force: true });
      }
      callback();
    },
    async getUser() {
      try {
        const token = this.$route.query.token;
        if (token) {
          console.log(token);
          await this.$axios
            .get(`/api/auth/reset_password`, {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            })
            .then((res) => {
              if (res.data.success) {
                this.user = res.data.user;
                this.form.setFieldsValue({
                  email: this.user.email,
                });
              }
            });
        }
      } catch (e) {
        console.log(e);
        this.$message.error(e.message);
      }
    },
    async resetPassword(form) {
      try {
        this.loading = true;
        await this.$axios
          .post("/api/auth/reset_password", form)
          .then(async (res) => {
            if (res.data.success) {
              this.$message.success(res.data.message);
              await this.$auth.loginWith("local", {
                data: {
                  username: form.email,
                  password: form.password,
                },
              });
            } else {
              this.$message.error(data.message);
            }
          });
      } catch (e) {
        console.log(e);
        this.$message.error(e.message);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
#expressly-reset-password .reset-password-form {
  max-width: 300px;
}
#expressly-reset-password .reset-password-form-forgot {
  float: right;
}
#expressly-reset-password .reset-password-form-button {
  width: 100%;
}
</style>
