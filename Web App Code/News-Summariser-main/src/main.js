/**
=========================================================
* Vue Soft UI Dashboard - v3.0.0
=========================================================

* Product Page: https://creative-tim.com/product/vue-soft-ui-dashboard
* Copyright 2022 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";
import Vue from "vue";
import vSelect from "vue-select";

import 'vue-select/dist/vue-select.css';

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import "./assets/css/nucleo-icons.css";
import "./assets/css/nucleo-svg.css";
import SoftUIDashboard from "./soft-ui-dashboard";


const appInstance = createApp(App);
appInstance.component('v-select', vSelect)
appInstance.use(store);
appInstance.use(FontAwesomeIcon);
appInstance.use(router);
appInstance.use(SoftUIDashboard);
appInstance.mount("#app");
