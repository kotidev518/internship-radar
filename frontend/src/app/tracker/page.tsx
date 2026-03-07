"use client";

import { useState, useEffect } from "react";
import { applicationAPI } from "@/lib/api";
import { motion } from "framer-motion";

const STATUSES = ["saved", "applied", "interview", "rejected", "offer"];

export default function Tracker() {
    const [applications, setApplications] = useState<any[]>([]);

    useEffect(() => {
        fetchApps();
    }, []);

    const fetchApps = async () => {
        try {
            const data = await applicationAPI.getAll();
            setApplications(data);
        } catch (error) {
            console.error(error);
        }
    };

    const handleDragStart = (e: React.DragEvent, id: number) => {
        e.dataTransfer.setData("app_id", id.toString());
    };

    const handleDrop = async (e: React.DragEvent, status: string) => {
        const idStr = e.dataTransfer.getData("app_id");
        if (!idStr) return;
        const id = parseInt(idStr, 10);

        // Optimistic UI update
        setApplications(prev => prev.map(app => app.id === id ? { ...app, status } : app));

        try {
            await applicationAPI.updateStatus(id, status);
        } catch (error) {
            console.error("Status update failed", error);
            fetchApps(); // Revert on failure
        }
    };

    const allowDrop = (e: React.DragEvent) => {
        e.preventDefault();
    };

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-white mb-2">Application Tracker</h1>
                <p className="text-slate-400">Drag and drop to track your pipeline.</p>
            </div>

            <div className="flex gap-4 overflow-x-auto pb-4 h-[calc(100vh-200px)]">
                {STATUSES.map((status) => {
                    const columnApps = applications.filter((app) => app.status === status);
                    return (
                        <div
                            key={status}
                            className="flex-1 min-w-[300px] flex flex-col bg-slate-900/50 rounded-xl border border-slate-800 p-4"
                            onDrop={(e) => handleDrop(e, status)}
                            onDragOver={allowDrop}
                        >
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="font-semibold text-slate-200 capitalize tracking-wide">{status}</h3>
                                <span className="bg-slate-800 text-xs px-2 py-1 rounded-full text-slate-400">
                                    {columnApps.length}
                                </span>
                            </div>

                            <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
                                {columnApps.map((app) => (
                                    <motion.div
                                        layoutId={`app-${app.id}`}
                                        key={app.id}
                                        draggable
                                        onDragStart={(e: any) => handleDragStart(e, app.id)}
                                        className="bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 p-4 rounded-lg cursor-grab active:cursor-grabbing transition-colors"
                                    >
                                        <h4 className="font-medium text-white line-clamp-1">{app.internship.role}</h4>
                                        <p className="text-sm text-indigo-400 mb-2">{app.internship.company}</p>
                                        <div className="flex justify-between items-center text-xs text-slate-400">
                                            <span>{app.internship.location}</span>
                                            <span>{new Date(app.updated_at).toLocaleDateString()}</span>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
