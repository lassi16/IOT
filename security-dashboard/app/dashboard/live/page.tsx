import type { Metadata } from "next"
import DashboardLayout from "@/components/dashboard-layout"
import LiveCameraView from "@/components/live-camera-view"

export const metadata: Metadata = {
  title: "Live Camera | SecureView",
  description: "View your security cameras in real-time",
}

export default function LiveCameraPage() {
  return (
    <DashboardLayout>
      <div className="container mx-auto px-4 py-8">
        <h1 className="mb-6 text-3xl font-bold text-white">Live Camera Feed</h1>
        <p className="mb-8 text-gray-400">View real-time footage from your security cameras</p>
        <LiveCameraView />
      </div>
    </DashboardLayout>
  )
}

