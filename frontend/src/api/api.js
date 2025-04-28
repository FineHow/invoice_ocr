// api.js
const baseURL = process.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export const fetchInvoice = async (invoiceId) => {
    const response = await fetch(`${baseURL}/api/v1/invoices/${invoiceId}`);
    return response.json();
};

export const uploadImage = async (file) => {
    const formData = new FormData();
    formData.append("image_file", file);
    
    const response = await fetch(`${baseURL}/api/v1/images/upload-image`, {
        method: "POST",
        body: formData,
    });
    return response.json();
};