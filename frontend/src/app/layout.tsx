import { Dispatch, SetStateAction, createContext, useState } from "react";
import "./globals.css";
import { Inter } from "next/font/google";
import { Metadata } from "next";
import { Analytics } from "@vercel/analytics/react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FitAI",
  description: "Elevate your fitness game with a custom workout plan",
  themeColor: "#d1c1d7",
  openGraph: {
    type: "website",
    title: "FitAI",
    description: "Elevate your fitness game with a custom workout plan",
    url: "https://fit-ai-omega.vercel.app/",
    images: "/opengraph-image.png",
  },
  twitter: {
    title: "FitAI",
    description: "Elevate your fitness game with a custom workout plan",
    card: "summary",
    images: "/opengraph-image.png",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="pastel">
      <body
        className={`${inter.className} -z-20 relative flex flex-col items-center bg-base-200`}
      >
        {children}
        <Analytics />
      </body>
    </html>
  );
}
