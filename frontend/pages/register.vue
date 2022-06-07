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
              'userName',
              {
                rules: [
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
          </a-input> </a-form-item
        ><a-form-item>
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
          <a-input
            v-decorator="[
              'confirmpassword',
              {
                rules: [
                  {
                    required: true,
                    message: 'Please input your confirm Password!',
                  },
                ],
              },
            ]"
            type="password"
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
          >
            Register
          </a-button>
          Or
          <router-link to="/login"> login now! </router-link>
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
        { hid: "description", name: "description", content: "Landing Page" },
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
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
        }
      });
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
