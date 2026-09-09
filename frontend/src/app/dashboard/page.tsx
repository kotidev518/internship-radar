"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { internshipAPI, applicationAPI } from "@/lib/api";
import { MapPin, Briefcase, Tag, Save, Send } from "lucide-react";

interface InternshipItem {
    id: number;
    role: string;
    company: string;
    category: string;
    location: string;
    remote: boolean;
    stipend?: string;
    skills?: string[];
    apply_link: string;
}

export default function Dashboard() {
    const [internships, setInternships] = useState<InternshipItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");

    useEffect(() => {
        fetchInternships();
    }, []);

    const fetchInternships = async () => {
        setLoading(true);
        try {
            const data = await internshipAPI.getAll();
            setInternships(data);
        } catch (error) {
            console.error("Failed to fetch internships", error);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await internshipAPI.search({ q: search });
            setInternships(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async (id: number) => {
        try {
            await applicationAPI.create(id, "saved");
            alert("Saved to Tracker!");
        } catch {
            alert("Already tracked or error occurred.");
        }
    };

    const handleApply = async (id: number, link: string) => {
        window.open(link, '_blank');
        try {
            await applicationAPI.create(id, "applied");
        } catch (error) {
            console.error("Failed to update application status to applied", error);
        }
    };

    const handleScrape = async () => {
        try {
            alert("Starting realtime scrape in the background. This will take a few minutes...");
            const response = await internshipAPI.triggerScrape();
            console.log("Scrape triggered:", response);
        } catch (error) {
            console.error("Failed to start scrape:", error);
            alert("Failed to start scrape.");
        }
    };

    return (
        <div className="space-y-8">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Discover Internships</h1>
                    <p className="text-slate-400">Find your next big opportunity curated by AI.</p>
                </div>
                <form onSubmit={handleSearch} className="flex gap-2 w-full md:w-auto">
                    <button type="button" onClick={handleScrape} className="px-4 py-2 bg-pink-600 hover:bg-pink-700 text-white rounded-lg font-medium shadow-lg shadow-pink-500/20 transition-all whitespace-nowrap">
                        Fetch Realtime
                    </button>
                    <input
                        type="text"
                        placeholder="Search roles, companies..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="w-full md:w-64 px-4 py-2 rounded-lg bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
                    />
                    <button type="submit" className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-colors">
                        Search
                    </button>
                </form>
            </div>

            {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3, 4, 5, 6].map((i) => (
                        <div key={i} className="h-64 rounded-xl bg-slate-900/50 animate-pulse border border-slate-800" />
                    ))}
                </div>
            ) : internships.length === 0 ? (
                <div className="text-center py-20">
                    <p className="text-slate-400 text-lg">No internships found matching your criteria.</p>
                </div>
            ) : (
                <motion.div
                    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                    initial="hidden"
                    animate="visible"
                    variants={{
                        hidden: { opacity: 0 },
                        visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
                    }}
                >
                    <AnimatePresence>
                        {internships.map((internship: InternshipItem) => (
                            <motion.div
                                key={internship.id}
                                variants={{
                                    hidden: { opacity: 0, y: 20 },
                                    visible: { opacity: 1, y: 0 }
                                }}
                                whileHover={{ y: -5, transition: { duration: 0.2 } }}
                                className="group relative rounded-xl bg-slate-900/80 border border-slate-800 p-6 flex flex-col hover:border-indigo-500/50 hover:shadow-[0_0_30px_-5px_rgba(99,102,241,0.2)] transition-all overflow-hidden backdrop-blur-sm"
                            >
                                {/* Glow effect */}
                                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-32 bg-indigo-500/20 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity" />

                                <div className="flex justify-between items-start mb-4 relative z-10">
                                    <div>
                                        <h3 className="text-xl font-bold text-white mb-1 line-clamp-1">{internship.role}</h3>
                                        <p className="text-indigo-400 font-medium">{internship.company}</p>
                                    </div>
                                    <span className="px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                                        {internship.category}
                                    </span>
                                </div>

                                <div className="space-y-2 mb-6 flex-1 relative z-10">
                                    <div className="flex items-center text-sm text-slate-400">
                                        <MapPin className="w-4 h-4 mr-2" />
                                        {internship.location} {internship.remote ? "(Remote)" : ""}
                                    </div>
                                    {internship.stipend && (
                                        <div className="flex items-center text-sm text-emerald-400">
                                            <Briefcase className="w-4 h-4 mr-2" />
                                            {internship.stipend}
                                        </div>
                                    )}
                                    <div className="flex items-start text-sm text-slate-400 mt-3 pt-3 border-t border-slate-800/50">
                                        <Tag className="w-4 h-4 mr-2 mt-0.5 shrink-0" />
                                        <div className="flex flex-wrap gap-1">
                                            {(internship.skills || []).slice(0, 4).map((skill: string, i: number) => (
                                                <span key={i} className="px-2 py-0.5 rounded bg-slate-800/50 text-xs text-slate-300">
                                                    {skill}
                                                </span>
                                            ))}
                                            {(internship.skills || []).length > 4 && (
                                                <span className="px-2 py-0.5 rounded bg-slate-800/50 text-xs text-slate-500">
                                                    +{(internship.skills || []).length - 4}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                <div className="flex gap-3 relative z-10 mt-auto">
                                    <button
                                        onClick={() => handleSave(internship.id)}
                                        className="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium transition-colors"
                                    >
                                        <Save className="w-4 h-4" /> Save
                                    </button>
                                    <button
                                        onClick={() => handleApply(internship.id, internship.apply_link)}
                                        className="flex-[2] flex items-center justify-center gap-2 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-colors shadow-lg shadow-indigo-500/20"
                                    >
                                        <Send className="w-4 h-4" /> Apply Now
                                    </button>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </motion.div>
            )}
        </div>
    );
}
