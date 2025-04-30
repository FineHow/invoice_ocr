const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

//发票完整ocr识别接口
export const uploadInvoice = async (formData) => {
    const response = await fetch(`${baseURL}/api/v1/invoice/process_invoices/`, 
    {
        method: "POST",
        body: formData,
        mode: "cors"  // 确保启用了跨域
    });
    const data = await response.json();
    return data;

};

