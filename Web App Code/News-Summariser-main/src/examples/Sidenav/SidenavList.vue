<template>
  <div
    class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100"
    id="sidenav-collapse-main"
  >
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-collapse navText="News Search" :to="{ name: 'News Search' }">
          <template #icon>
            <Search  />
          </template>
        </sidenav-collapse>
      </li>
    </ul>
  </div>
</template>
<script>
import SidenavCollapse from "./SidenavCollapse.vue";

// import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
// import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

export default {
  name: "SidenavList",
  props: {
    cardBg: String,
  },
  data() {
    return {
      title: "Smart Monitoring System",
      controls: "dashboardsExamples",
      isActive: "active",
      type: ""
    };
  },
  components: {
    SidenavCollapse,
    // SidenavCard,
    // Shop,
  },
  methods: {
    getRoute() {
      const routeArr = this.$route.path.split("/");
      return routeArr[1];
      
    },
    // for debugging
    typepr(){
      if(JSON.parse(localStorage.getItem("userInfo"))){
        this.type=JSON.parse(localStorage.getItem("userInfo"))['type'],
        console.log(this.type)
      }
      
    },
  },
  created() {
    this.typepr()
  },
};

</script>
