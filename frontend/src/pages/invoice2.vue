<template>
    <div class="container">
      <h2>批量发票识别_两个字段</h2>
      <!-- <el-button type="primary" @click="push">去往上传页面</el-button> -->
      <form @submit.prevent="handleUpload">
        <input type="file" multiple @change="handleFileChange" />
        <el-button type="primary" @click="handleUpload">上传</el-button>
        <!-- <button type="submit">上传处理</button> -->
      </form>
      <div v-if="downloadUrl">
        <a :href="downloadUrl" target="_blank">
          <el-button type="success" icon="el-icon-download">
            下载结果 Excel
          </el-button>
        </a>
      </div>
      <div>{{ downloadUrl }}</div>
      <div v-if="ocrresult">
        <el-table :data="ocrresult" stripe tooltip-effect="dark" class="mt-10 table-default " width="1500px" >
            <el-table-column label="文件名" align="center" prop="file"/>
            <el-table-column label="页数" align="center" prop="page"/>
            <el-table-column label="发票号码" align="center" prop="text.invoice_number"/>
            <el-table-column label="开票日期" align="center" prop="text.invoice_date"/>
        </el-table>
      </div>
    </div>
  </template>
  
  <script>
  import {uploadInvoice} from "../api/api.js";
  export default {
  
    
    data() {
      return {
        files: [],
        language: "chi_sim",
        downloadUrl: null,
        ocrresult:  [],
      };
    },
  
  
    methods: {
      handleFileChange(event) {
        this.files = event.target.files;
      },
      push() {
        this.$router.push({ path: "/upload" });
      },
      
      async handleUpload() {
        const formData = new FormData();
        for (let file of this.files) {
          formData.append("files", file);
        }
        formData.append("language", this.language);
        try {
            const response = await uploadInvoice(formData);
              this.downloadUrl = response.data.download_link;//下载链接
              this.ocrresult = response.data.extracted_data;//识别结果
          } catch (error) {
            console.error("处理发票失败:", error);
          }
      },
    },
  };
  </script>
  
  <style>
  .container {
    /* max-width: 1600px; */
    margin: 20px auto;
  }
  </style>
  