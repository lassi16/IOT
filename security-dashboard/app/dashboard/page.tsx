import type { Metadata } from "next"
import DashboardLayout from "@/components/dashboard-layout"
import DashboardOptions from "@/components/dashboard-options"

export const metadata: Metadata = {
  title: "Dashboard | SecureView",
  description: "Security camera dashboard",
}

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="container mx-auto px-4 py-8">
        <h1 className="mb-6 text-3xl font-bold text-white">Security Dashboard</h1>
        <p className="mb-8 text-gray-400">Monitor your security cameras and access recordings</p>
        <DashboardOptions />
      </div>
    </DashboardLayout>
  )
}

