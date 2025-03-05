<template>
  <div id="app">
    <router - link to="/structural-search">结构式搜索</router - link>
    <router - view></router - view>
  </div>
</template>
<script>
import StructureSearch from './views/StructureSearch.vue';

export default {
  components: {
    StructureSearch
  }
};
</script>