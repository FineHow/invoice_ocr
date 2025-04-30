<template>
  <div class="common-layout">
    <el-container class="layout-container-demo">
      <el-header >
        <h1>🚀ocr功能测试demo页面</h1>
      </el-header>
      <el-container  style="height: 500px">
        <el-aside width="200px">
          <el-menu :default-active="$route.path" router  text-color="#333" active-text-color="#409EFF">
            <el-menu-item index="/"><router-link to="/">首页</router-link></el-menu-item>
            <el-menu-item index="/invoice"><router-link to="/invoice">批量发票识别系统</router-link></el-menu-item>
            <el-menu-item index="/ocr"><router-link to="/ocr">全文普通ocr</router-link></el-menu-item>
            <el-menu-item index="/mark"><router-link to="/mark">mark相机月度核销</router-link></el-menu-item>
            <el-menu-item index="/invoice2"><router-link to="/invoice2">发票识别_单两个字段</router-link></el-menu-item>
            <el-menu-item index="/about"><router-link to="/about">关于使用</router-link></el-menu-item>
          </el-menu>
        </el-aside>
      <el-container>
          <el-main style="padding: 20px; width: 1500px;">
            <router-view></router-view>
          </el-main>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<style>
/* 添加一些基本样式 */
.common-layout{
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.common-layout .el-header {
  background-color: var(--el-color-primary-light-8);
  color: #606266;
  padding: 20px;
  margin: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
}

</style>