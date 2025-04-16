import { createApp } from 'vue'; // Vue 3 的 createApp 方法
import './style.css'; // 项目的样式文件
import App from './App.vue'; // 根组件

// 引入 Element Plus 和样式
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

// 创建 Vue 应用
const app = createApp(App);

// 注册 Element Plus
app.use(ElementPlus);

// 挂载应用到 DOM
app.mount('#app');