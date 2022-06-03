<template>
  <article>
    <div style="padding: 20px">
      <a-row :gutter="16">
        <a-col :span="12">
          <a-card title="Church" :bordered="true">
            <p>
              <nuxt-link to="search/church"> Book spot in church</nuxt-link>
            </p>
          </a-card>
        </a-col>
        <a-col :span="12">
          <a-card title="Office" :bordered="true">
            <p>
              <nuxt-link to="search/space"> Book space in line</nuxt-link>
            </p>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </article>
</template>
