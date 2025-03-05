import { createRouter, createWebHistory } from 'vue-router';
import StructureSearch from '@/views/StructureSearch.vue';

const routes = [
  {
    path: '/structural-search',
    name: 'StructureSearch',
    component: StructureSearch
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;