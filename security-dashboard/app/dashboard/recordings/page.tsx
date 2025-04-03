import type { Metadata } from "next"
import DashboardLayout from "@/components/dashboard-layout"
import RecordingsView from "@/components/recordings-view"

export const metadata: Metadata = {
  title: "Recordings | SecureView",
  description: "View your security camera recordings",
}

export default function RecordingsPage() {
  return (
    <DashboardLayout>
      <div className="container mx-auto px-4 py-8">
        <h1 className="mb-6 text-3xl font-bold text-white">Recordings & Motion Clips</h1>
        <p className="mb-8 text-gray-400">Browse and view your recorded security footage</p>
        <RecordingsView />
      </div>
    </DashboardLayout>
  )
}

