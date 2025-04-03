"use client"

import { useRouter } from "next/navigation"
import { Camera, Video } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

// Note: We're simulating framer-motion here since it's not available in the sandbox
// In a real project, you would install and import framer-motion
const MotionCard = ({ children, ...props }: any) => {
  return (
    <div className="transform transition-all duration-300 hover:scale-105 hover:shadow-lg" {...props}>
      {children}
    </div>
  )
}

export default function DashboardOptions() {
  const router = useRouter()

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <MotionCard>
        <Card
          className="cursor-pointer border border-gray-800 bg-gray-900/50 shadow-lg hover:border-blue-600/50"
          onClick={() => router.push("/dashboard/live")}
        >
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center text-2xl text-white">
              <Camera className="mr-2 h-6 w-6 text-blue-500" />
              Live Security Camera
            </CardTitle>
            <CardDescription className="text-gray-400">
              View real-time footage from your security cameras
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="aspect-video overflow-hidden rounded-lg bg-gray-800">
              <div className="flex h-full items-center justify-center">
                <div className="text-center">
                  <div className="mb-2 animate-pulse rounded-full bg-blue-600/20 p-4">
                    <Camera className="h-8 w-8 text-blue-500" />
                  </div>
                  <p className="text-sm text-gray-400">Click to view live feed</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </MotionCard>

      <MotionCard>
        <Card
          className="cursor-pointer border border-gray-800 bg-gray-900/50 shadow-lg hover:border-blue-600/50"
          onClick={() => router.push("/dashboard/recordings")}
        >
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center text-2xl text-white">
              <Video className="mr-2 h-6 w-6 text-blue-500" />
              Recordings & Motion Clips
            </CardTitle>
            <CardDescription className="text-gray-400">
              Access past recordings and motion-detected events
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="aspect-video overflow-hidden rounded-lg bg-gray-800">
              <div className="grid grid-cols-2 grid-rows-2 gap-1 p-1">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="aspect-video rounded bg-gray-700/50">
                    <div className="flex h-full items-center justify-center">
                      <div className="h-1 w-full max-w-[80%] rounded-full bg-gray-600">
                        <div className="h-1 w-1/3 rounded-full bg-blue-500"></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </MotionCard>
    </div>
  )
}

