// components/PageLoading.tsx
"use client";

import { motion } from "framer-motion";

export function PageLoading() {
  return (
    <motion.div
      className="fixed top-0 left-0 right-0 z-50 h-1 bg-gradient-to-r from-blue-400 to-purple-600"
      initial={{ scaleX: 0, transformOrigin: "0%" }}
      animate={{
        scaleX: 1,
        transition: { duration: 0.5, ease: "easeInOut" }
      }}
    />
  );
}