<template>
  <div class="py-2 container-fluid">
    <div class="row px-1">
      <searchbar/>
    </div>
  </div>
</template>

<script>
// import AuthorsTable from "./components/AuthorsTable";
// import ProjectsTable from "./components/ProjectsTable";
import Searchbar from "./components/Searchbar";

export default {
  name: "tables",
  components: {
    Searchbar
  },
};
</script>
