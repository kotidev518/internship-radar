import axios from "axios";

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
    headers: {
        "Content-Type": "application/json",
    },
});

export const internshipAPI = {
    getAll: async (skip = 0, limit = 50) => {
        const res = await api.get(`/internships`, { params: { skip, limit } });
        return res.data;
    },
    search: async (params: any) => {
        const res = await api.get(`/internships/search`, { params });
        return res.data;
    },
};

export const applicationAPI = {
    getAll: async () => {
        const res = await api.get(`/applications`);
        return res.data;
    },
    create: async (internship_id: number, status: string = "saved") => {
        const res = await api.post(`/applications`, { internship_id, status });
        return res.data;
    },
    updateStatus: async (id: number, status: string) => {
        const res = await api.patch(`/applications/${id}/status`, { status });
        return res.data;
    },
};
