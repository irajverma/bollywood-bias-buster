import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { ThemeToggle } from "@/components/theme-toggle"
import { Toaster } from "@/components/ui/toaster"
import Link from "next/link"
import { Film, BarChart3, FileText, Wrench, Database, Home } from "lucide-react"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Bollywood Bias Buster",
  description: "Analyze and eliminate gender bias in Bollywood cinema through AI-powered script analysis",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <div className="min-h-screen bg-background">
            {/* Navigation */}
            <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
              <div className="container mx-auto px-4">
                <div className="flex h-16 items-center justify-between">
                  <div className="flex items-center space-x-8">
                    <Link href="/" className="flex items-center space-x-2">
                      <Film className="h-6 w-6 text-primary" />
                      <span className="font-bold text-xl">Bollywood Bias Buster</span>
                    </Link>

                    <div className="hidden md:flex items-center space-x-6">
                      <Link
                        href="/"
                        className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                      >
                        <Home className="h-4 w-4" />
                        <span>Home</span>
                      </Link>
                      <Link
                        href="/analyze"
                        className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                      >
                        <FileText className="h-4 w-4" />
                        <span>Analyze</span>
                      </Link>
                      <Link
                        href="/dashboard"
                        className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                      >
                        <BarChart3 className="h-4 w-4" />
                        <span>Dashboard</span>
                      </Link>
                      <Link
                        href="/data-explorer"
                        className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                      >
                        <Database className="h-4 w-4" />
                        <span>Data Explorer</span>
                      </Link>
                      <Link
                        href="/rewrite"
                        className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                      >
                        <Wrench className="h-4 w-4" />
                        <span>Rewrite</span>
                      </Link>
                      <Link
                        href="/reports"
                        className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                      >
                        <FileText className="h-4 w-4" />
                        <span>Reports</span>
                      </Link>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    <ThemeToggle />
                  </div>
                </div>
              </div>
            </nav>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-8">{children}</main>
          </div>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  )
}
