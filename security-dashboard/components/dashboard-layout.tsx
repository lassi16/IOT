"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Bell, Camera, Home, LogOut, Menu, Settings, Video } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: Home },
    { name: "Live Camera", href: "/dashboard/live", icon: Camera },
    { name: "Recordings", href: "/dashboard/recordings", icon: Video },
    { name: "Settings", href: "/dashboard/settings", icon: Settings },
  ]

  return (
    <div className="flex min-h-screen bg-gray-950">
      {/* Sidebar for desktop */}
      <div className="hidden w-64 flex-col bg-gray-900 md:flex">
        <div className="flex h-16 items-center px-6">
          <Link href="/dashboard" className="flex items-center">
            <span className="text-xl font-bold text-white">SecureView</span>
          </Link>
        </div>
        <div className="flex flex-1 flex-col justify-between p-4">
          <nav className="space-y-1">
            {navigation.map((item) => {
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`group flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                    isActive ? "bg-blue-600 text-white" : "text-gray-300 hover:bg-gray-800 hover:text-white"
                  }`}
                >
                  <item.icon
                    className={`mr-3 h-5 w-5 ${isActive ? "text-white" : "text-gray-400 group-hover:text-white"}`}
                  />
                  {item.name}
                </Link>
              )
            })}
          </nav>
          <div className="mt-auto">
            <Link
              href="/"
              className="group flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-800 hover:text-white"
            >
              <LogOut className="mr-3 h-5 w-5 text-gray-400 group-hover:text-white" />
              Logout
            </Link>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
        <SheetTrigger asChild>
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-6 w-6 text-gray-300" />
            <span className="sr-only">Open menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 border-gray-800 bg-gray-900 p-0">
          <div className="flex h-16 items-center border-b border-gray-800 px-6">
            <Link href="/dashboard" className="flex items-center" onClick={() => setIsMobileMenuOpen(false)}>
              <span className="text-xl font-bold text-white">SecureView</span>
            </Link>
          </div>
          <div className="flex flex-1 flex-col justify-between p-4">
            <nav className="space-y-1">
              {navigation.map((item) => {
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`group flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                      isActive ? "bg-blue-600 text-white" : "text-gray-300 hover:bg-gray-800 hover:text-white"
                    }`}
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <item.icon
                      className={`mr-3 h-5 w-5 ${isActive ? "text-white" : "text-gray-400 group-hover:text-white"}`}
                    />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
            <div className="mt-auto">
              <Link
                href="/"
                className="group flex items-center rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-800 hover:text-white"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                <LogOut className="mr-3 h-5 w-5 text-gray-400 group-hover:text-white" />
                Logout
              </Link>
            </div>
          </div>
        </SheetContent>
      </Sheet>

      {/* Main content */}
      <div className="flex flex-1 flex-col">
        {/* Top navigation */}
        <header className="border-b border-gray-800 bg-gray-900">
          <div className="flex h-16 items-center justify-between px-4">
            <div className="flex items-center md:hidden">
              <Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
                <SheetTrigger asChild>
                  <Button variant="ghost" size="icon">
                    <Menu className="h-6 w-6 text-gray-300" />
                    <span className="sr-only">Open menu</span>
                  </Button>
                </SheetTrigger>
              </Sheet>
              <span className="ml-2 text-lg font-medium text-white">SecureView</span>
            </div>
            <div className="flex items-center">
              <Button variant="ghost" size="icon" className="text-gray-300 hover:text-white">
                <Bell className="h-5 w-5" />
                <span className="sr-only">Notifications</span>
              </Button>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-gradient-to-br from-gray-900 to-gray-950">{children}</main>
      </div>
    </div>
  )
}

