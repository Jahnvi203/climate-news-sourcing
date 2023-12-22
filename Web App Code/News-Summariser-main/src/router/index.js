import { createRouter, createWebHistory } from "vue-router";

import NewsSearch from "@/views/NewsSearch.vue";
import Entity from "@/views/Entity.vue";

const routes = [
  {
    path: "/",
    name: "News Search",
    component: NewsSearch,
  },
  {
    path: "/entity",
    name: "Entity",
    component: Entity,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

export default router;
