import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/ui/Navbar";

export const metadata: Metadata = {
  title: "GTNIC SOC | Cybersecurity Threat Triage & Incident Response",
  description:
    "Autonomous Security Operations Center console for real-time threat triage, alert correlation, and SOAR mitigation orchestration.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#070b12] text-slate-200 font-sans antialiased selection:bg-emerald-500/20 selection:text-emerald-300">
        <Navbar />
        <main className="max-w-[1800px] mx-auto px-3 sm:px-6 lg:px-8 py-5">
          {children}
        </main>
      </body>
    </html>
  );
}
