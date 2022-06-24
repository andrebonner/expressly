<template>
  <section>
    <a-row :gutter="6" :style="{ padding: '10px 0' }">
      <a-col :span="12">
        <AreaList />
      </a-col>
      <a-col :span="12">
        <InstitutionList />
      </a-col> </a-row
    ><a-row :gutter="6" :style="{ padding: '10px 0' }">
      <a-col :span="12">
        <ScheduleList />
      </a-col>
      <a-col :span="12">
        <UserList />
      </a-col>
    </a-row>
  </section>
</template>
<script>
import AreaList from "~/components/admin/AreaList.vue";
import InstitutionList from "~/components/admin/InstitutionList.vue";
import ScheduleList from "~/components/admin/ScheduleList.vue";
import UserList from "~/components/admin/UserList.vue";
export default {
  head() {
    return {
      titleTemplate: "%s - Admin",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { hid: "description", name: "description", content: "Admin" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    };
  },
  components: {
    AreaList,
    InstitutionList,
    ScheduleList,
    UserList,
  },
  middleware: ["admin-auth"],
};
</script>
