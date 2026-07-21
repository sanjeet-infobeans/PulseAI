import type { Metadata } from "next"
import { Lexend } from "next/font/google"
import "./globals.css"
import { QueryProvider } from "@/components/layout/query-provider"

const lexend = Lexend({
  subsets: ["latin"],
  weight: ["300", "400", "500"],
  variable: "--font-lexend",
  display: "swap",
})

export const metadata: Metadata = {
  title: "PulseAI",
  description: "AI-powered project delivery intelligence — InfoBeans",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={lexend.variable}>
      <body className="font-sans antialiased bg-background text-charcoal">
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  )
}
