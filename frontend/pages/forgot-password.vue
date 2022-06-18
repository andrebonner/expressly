<template>
  <section>
    <a-card :style="{ width: '450px', margin: ' 10px auto', padding: '10px' }">
      <a-form
        id="expressly-forgot-pwd"
        :form="form"
        class="forgot-pwd-form"
        @submit="handleSubmit"
      >
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
              type="user"
              style="color: rgba(0, 0, 0, 0.25)"
            />
          </a-input>
        </a-form-item>
        <a-form-item>
          <nuxt-link class="forgot-pwd-form-forgot" to="/login">
            Log in
          </nuxt-link>
          <a-button
            type="primary"
            html-type="submit"
            class="forgot-pwd-form-button"
          >
            Forgot password
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
      titleTemplate: "%s - Forgot Password",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Forgot Password" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this);
  },

  methods: {
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
          this.forgotPassword(values);
        }
      });
    },
    async forgotPassword(form) {
      this.loading = true;
      try {
        const { email } = form;
        await this.$axios
          .post("/api/auth/forgot_password", { email })
          .then((res) => {
            if (res.data.success) {
              this.$message.success(
                "Please check your email to reset password"
              );
              this.$router.push("/login");
            } else {
              this.$message.error(res.data.message);
            }
          });
      } catch (error) {
        this.$message.error(error.response.data.message);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style>
#expressly-forgot-pwd .forgot-pwd-form {
  max-width: 300px;
}
#expressly-forgot-pwd .forgot-pwd-form-forgot {
  float: right;
}
#expressly-forgot-pwd .forgot-pwd-form-button {
  width: 100%;
}
</style>
