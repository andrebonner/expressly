<template>
  <section>
    <a-card :style="{ width: '450px', margin: ' 10px auto', padding: '10px' }">
      <a-form
        id="expressly-register"
        :form="form"
        class="register-form"
        @submit="handleSubmit"
      >
        <a-form-item>
          <a-input
            v-decorator="[
              'name',
              {
                rules: [{ required: true, message: 'Please input your name!' }],
              },
            ]"
            placeholder="Name"
          >
            <a-icon
              slot="prefix"
              type="user"
              style="color: rgba(0, 0, 0, 0.25)"
            />
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-input
            v-decorator="[
              'email',
              {
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
            class="register-form-button"
            :loading="loading"
          >
            Register
          </a-button>
          Or
          <nuxt-link to="/login"> login now! </nuxt-link>
        </a-form-item>
      </a-form></a-card
    >
  </section>
</template>

<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Register",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Register" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "normal_register" });
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
          this.register(values);
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
    async register(form) {
      try {
        this.loading = true;
        await this.$axios.post("/api/auth/register", form).then(async (res) => {
          if (res.data.success) {
            this.$message.success(data.message);
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
        this.$message.error(e.message);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style>
#expressly-register .register-form {
  max-width: 300px;
}
#expressly-register .register-form-forgot {
  float: right;
}
#expressly-register .register-form-button {
  width: 100%;
}
</style>
