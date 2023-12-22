<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <searchbar />
      </div>
    </div>
  </div>
</template>

<script>

import Searchbar from "./components/Searchbar";

export default {
  name: "tables",
  components: {
    Searchbar,
  },
};
</script>
