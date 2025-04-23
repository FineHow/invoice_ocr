<template>
  <div class="container">
    <h1>-----------------批量发票识别系统--------------</h1>
    <!-- <el-button type="primary" @click="push">去往上传页面</el-button> -->
    <form @submit.prevent="handleUpload">
      <input type="file" multiple @change="handleFileChange" />
      <el-button type="primary" @click="handleUpload">上传</el-button>
      <!-- <button type="submit">上传处理</button> -->
    </form>
    <div v-if="downloadUrl">
      <a :href="downloadUrl">下载结果 Excel</a>
    </div>
    <div>{{ downloadUrl }}</div>
    <div v-if="ocrresult">
      <el-table :data="ocrresult" stripe tooltip-effect="dark" class="mt-10 table-default " width="1500px" >
				<el-table-column label="文件名" align="center" prop="file"/>
				<el-table-column label="页数" align="center" prop="page"/>
				<el-table-column label="发票号码" align="center" prop="text.invoice_number"/>
        <el-table-column label="开票日期" align="center" prop="text.invoice_date"/>
        <el-table-column label="购买方名称" align="center" prop="text.buyer_name"/>
				<el-table-column label="纳税人识别号" align="center" prop="text.buyer_tax_number"/>
				<el-table-column label="金额" align="center" prop="text.amount"/>
				<el-table-column label="税率" align="center" prop="text.tax_rate"/>
				<el-table-column label="税额" align="center" prop="text.tax_amount"/>
				
				
			</el-table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

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
        const response = await axios.post("http://localhost:8000/process_invoices/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
              console.log("请求成功:", response.data.extracted_data);
              this.downloadUrl = response.data.excel_file_path;
              this.ocrresult = response.data.data.extracted_data;
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
