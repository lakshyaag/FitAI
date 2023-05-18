import "./globals.css"
import { Inter } from "next/font/google"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "FitAI",
  description: "Elevate your fitness game with a custom workout plan",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" data-theme="pastel">
      <body
        className={`${inter.className} flex flex-col items-center bg-base-200`}
      >
        {children}
      </body>
    </html>
  )
}
