// components/ClientLayout.tsx
"use client";
import { Suspense } from "react";
import { AnimatedLayout } from "./AnimatedLayout";
import { PageLoading } from "./PageLoading";
import { Link } from "@nextui-org/link";

export function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <Suspense fallback={<PageLoading />}>
      <AnimatedLayout>
        <main className="container mx-auto max-w-7xl pt-16 px-6 flex-grow">
          {children}
        </main>
        <footer className="w-full flex items-center justify-center py-3">
          <Link
            isExternal
            className="flex items-center gap-1 text-current hover:opacity-80 transition-opacity"
            href="https://easyui.pro"
            title="easyui.pro homepage"
          >
            <span className="text-default-600">Powered by</span>
            <p className="text-primary bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
              Easy UI
            </p>
          </Link>
        </footer>
      </AnimatedLayout>
    </Suspense>
  );
}