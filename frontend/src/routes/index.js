import { createRouter, createWebHistory } from 'vue-router';
import Home from '../pages/Home.vue';
import About from '../pages/About.vue';
import Invoice from '../pages/invoice_all.vue';
import Ocr from '../pages/normalocr.vue';
import Mark from '../pages/mark.vue';
import Invoice2 from '../pages/invoice2.vue';

const routes = [
  // 首页
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  // 关于使用说明
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  // 发票识别
  {
    path: '/invoice',
    name: 'Invoice',
    component: Invoice,
  },
  // 普通OCR识别
  {
    path: '/ocr',
    name: 'Ocr',
    component: Ocr,
  },
  // mark相机识别
  {
    path: '/mark',
    name: 'Mark',
    component: Mark,
  },
    // 发票识别2_单两个字段
  {
    path: '/invoice2',
    name: 'Invoice2',
    component: Invoice2,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;