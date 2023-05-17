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
    <html lang="en" data-theme="fantasy">
      <body className={`${inter.className} py-4 flex flex-col items-center`}>
        {children}
      </body>
    </html>
  )
}
