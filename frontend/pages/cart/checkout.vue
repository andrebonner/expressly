<template>
  <article>
    <a-row>
      <a-col :style="{}">
        <div
          :style="{
            textAlign: 'center',
            margin: ' 0px auto',
            maxWidth: '500px',
          }"
        >
          <a-avatar :size="64" icon="check" />
          <h1>Thank you for the purchase!</h1>
          <p>You will receive an email confirmation shortly.</p>
          <a-button type="primary" block> Continue Shopping </a-button>
        </div>
      </a-col>
    </a-row>
  </article>
</template>
