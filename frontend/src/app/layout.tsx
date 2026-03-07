import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { LayoutDashboard, ListTodo } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Internship Radar",
  description: "Discover and track internships efficiently",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-slate-950 text-slate-50 min-h-screen flex flex-col antialiased`}>
        {/* Top Navbar */}
        <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/50 backdrop-blur supports-[backdrop-filter]:bg-slate-950/50">
          <div className="container flex h-16 max-w-7xl mx-auto items-center justify-between px-4 sm:px-6 lg:px-8">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                <span className="font-bold text-white text-lg">IR</span>
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
                Internship Radar
              </span>
            </div>
          </div>
        </header>

        <div className="flex flex-1 max-w-7xl mx-auto w-full">
          {/* Sidebar */}
          <aside className="hidden w-64 flex-col border-r border-slate-800 bg-slate-950/30 p-4 md:flex">
            <nav className="flex flex-col gap-2 relative">
              <Link
                href="/dashboard"
                className="flex items-center gap-3 rounded-lg px-3 py-2 text-slate-300 transition-all hover:bg-slate-800 hover:text-white"
              >
                <LayoutDashboard className="h-4 w-4 text-indigo-400" />
                Dashboard
              </Link>
              <Link
                href="/tracker"
                className="flex items-center gap-3 rounded-lg px-3 py-2 text-slate-300 transition-all hover:bg-slate-800 hover:text-white"
              >
                <ListTodo className="h-4 w-4 text-purple-400" />
                Application Tracker
              </Link>
            </nav>
          </aside>

          {/* Main Content */}
          <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
