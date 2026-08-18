import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "@/components/layout/AppShell";

export const metadata: Metadata = {
  title: "AI OS — Autonomous Multi-Agent Operating System",
  description: "Enterprise Autonomous AI Platform where goals are decomposed into task graphs and executed by coordinated AI agents.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full bg-surface-subtle text-slate-900 antialiased font-sans">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
