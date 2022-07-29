<template>
  <section>
    <a-row><h1 :style="{ textAlign: 'center' }">Choose your Plan</h1></a-row>
    <a-row :gutter="12"
      ><a-col
        :span="8"
        v-for="(account_type, index) in account_types.filter(
          (account_type) => account_type.id !== 1
        )"
        :key="account_type.id"
      >
        <a-card>
          <h2>{{ account_type.name }}</h2>
          <h3>${{ account_type.price }}</h3>
          <p>{{ account_type.description }}</p>
          <a-button type="button" @click="handleSelectPlan(account_type)" block
            >Select Plan</a-button
          >
        </a-card>
      </a-col>
    </a-row>
    <a-modal v-model="visible" title="Payment" on-ok="handlePayment">
      <template slot="footer">
        <a-button
          key="submit"
          type="primary"
          :loading="loading"
          @click="handlePayment"
          ><a-icon type="credit-card" />Pay</a-button
        >
      </template>
      <a-form :form="paymentForm">
        <a-form-item label="Payment Method">
          <a-select
            style="width: 100%"
            :disabled="true"
            v-decorator="[
              'payment_method',
              {
                initialValue: 'credit_card',
                rules: [
                  { required: true, message: 'Please select payment method!' },
                ],
              },
            ]"
          >
            <a-select-option value="">Select Payment Method</a-select-option>
            <a-select-option value="alipay">Alipay</a-select-option>
            <a-select-option value="wechat">WeChat</a-select-option>
            <a-select-option value="credit_card">Credit Card</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="Credit Card Number">
          <a-input
            placeholder="Credit Card Number"
            :maxLength="16"
            v-decorator="[
              'credit_card_number',
              {
                initialValue: '',
                rules: [
                  {
                    required: true,
                    message: 'Please input credit card number!',
                  },
                  {
                    min: 16,
                    max: 19,
                    message: 'Please input 16 digits!',
                  },
                ],
              },
            ]"
          /> </a-form-item
        ><a-row>
          <a-col span="16">
            <a-form-item label="Credit Card Expiration">
              <a-month-picker
                :disabled-date="disabledDate"
                placeholder="MM/YY"
                format="MM/YY"
                valueFormat="MM/YY"
                v-decorator="[
                  'credit_card_expiry',
                  {
                    initialValue: '',
                    rules: [
                      {
                        required: true,
                        message: 'Please input credit card expiry!',
                      },
                    ],
                  },
                ]"
                style="width: 100%"
              /> </a-form-item
          ></a-col>
          <a-col span="8">
            <a-form-item label="Credit Card CVV">
              <a-input-password
                placeholder="CVV"
                v-decorator="[
                  'credit_card_cvv',
                  {
                    initialValue: '',
                    rules: [
                      {
                        required: true,
                        message: 'Please input credit card cvv!',
                      },
                      {
                        min: 3,
                        max: 3,
                        message: 'Please input 3 digits!',
                      },
                    ],
                  },
                ]"
              /> </a-form-item
          ></a-col>
        </a-row>
        <a-form-item label="Credit Card Holder">
          <a-input
            placeholder="Credit Card Holder"
            v-decorator="[
              'credit_card_holder',
              {
                initialValue: '',
                rules: [
                  {
                    required: true,
                    message: 'Please input credit card holder!',
                  },
                ],
              },
            ]"
          /> </a-form-item
      ></a-form>
    </a-modal>
  </section>
</template>
<script>
export default {
  head() {
    return {
      title: "Choose your Plan",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          hid: "description",
          name: "description",
          content: "Choose your Plan",
        },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  data() {
    return {
      visible: false,
      loading: false,
      account_types: [],
      plan: {
        id: null,
        name: "",
        price: 0,
      },
    };
  },
  methods: {
    async getAccountTypes() {
      await this.$axios.get("/api/users/account_types").then((response) => {
        this.account_types = response.data;
      });
    },
    handleSelectPlan(plan) {
      // TODO: change current plan
      this.plan = plan;
      if (this.$auth.loggedIn) {
        this.visible = true;
        this.paymentForm.setFieldsValue({
          payment_method: "credit_card",
        });
      } else {
        this.$message.error("You must be logged in to select a plan");
        this.$router.push({
          path: "/login",
          query: {
            redirect: this.$route.fullPath,
          },
        });
      }
    },
    handlePayment() {
      this.paymentForm.validateFields(async (err, values) => {
        if (!err) {
          this.loading = true;
          await this.$axios
            .put("/api/users/upgrade", {
              plan: this.plan.id,
              payment_method: values.payment_method,
              credit_card_number: values.credit_card_number,
              credit_card_expiry: values.credit_card_expiry,
              credit_card_cvv: values.credit_card_cvv,
              credit_card_holder: values.credit_card_holder,
            })
            .then((response) => {
              this.visible = false;
              this.$message.success("Upgrade Successful");
              this.$router.push("/");
            })
            .catch((error) => {
              this.$message.error(error.response.data.message);
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    disabledDate(current) {
      return current && current.valueOf() < Date.now();
    },
  },
  beforeCreate() {
    this.paymentForm = this.$form.createForm(this, { name: "paymentForm" });
  },
  mounted() {
    this.getAccountTypes();
  },
};
</script>
