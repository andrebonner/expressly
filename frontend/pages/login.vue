<template>
  <section>
    <a-card :style="{ width: '450px', margin: ' 10px auto', padding: '10px' }">
      <a-form
        id="expressly-login"
        :form="form"
        class="login-form"
        @submit="handleSubmit"
      >
        <a-form-item>
          <a-input
            v-decorator="[
              'username',
              {
                rules: [
                  {
                    type: 'email',
                    message: 'The input is not valid E-mail!',
                  },
                  { required: true, message: 'Please input your username!' },
                ],
              },
            ]"
            placeholder="Username"
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
              'password',
              {
                rules: [
                  { required: true, message: 'Please input your Password!' },
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
        <a-form-item>
          <a-checkbox
            v-decorator="[
              'remember',
              {
                valuePropName: 'checked',
                initialValue: true,
              },
            ]"
          >
            Remember me
          </a-checkbox>
          <nuxt-link class="login-form-forgot" to="/forgot-password">
            Forgot password
          </nuxt-link>
          <a-button type="primary" html-type="submit" class="login-form-button">
            Log in
          </a-button>
          Or
          <nuxt-link to="/register"> register now! </nuxt-link>
        </a-form-item>
      </a-form></a-card
    >
  </section>
</template>

<script>
export default {
  head() {
    return {
      titleTemplate: "%s - Login",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Login" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "normal_login" });
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
          this.login(values);
        }
      });
    },
    async login(form) {
      try {
        let response = await this.$auth.loginWith("local", {
          data: form,
        });
        const result = response.data;
        if (result.success) {
          this.$message.success(result.message);
          if (this.$route.query.redirect) {
            this.$router.push(this.$route.query.redirect);
          } else {
            this.$router.push("/");
          }
        } else {
          this.$message.error(result.message);
        }
      } catch (error) {
        this.$message.error(error.message);
      }
    },
  },
};
</script>
<style>
#expressly-login .login-form {
  max-width: 300px;
}
#expressly-login .login-form-forgot {
  float: right;
}
#expressly-login .login-form-button {
  width: 100%;
}
</style>
