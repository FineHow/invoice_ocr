import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  define: {
    'process.env': process.env,
    },
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000/', // 后端地址
        changeOrigin: true, // 改变Origin头以模拟同源
        secure: false, // 设置对HTTPS请求的支持
        rewrite: (path) => path.replace(/^\/api/, '') // 如果前端请求使用 `/api`，可重写路径
      }
    }
  }
})


