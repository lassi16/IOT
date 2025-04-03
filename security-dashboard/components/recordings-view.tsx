"use client"

import { useState } from "react"
import { Calendar, ChevronDown, Download, Filter, Play, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"

export default function RecordingsView() {
  const [viewType, setViewType] = useState<"grid" | "list">("grid")

  // Mock data for recordings
  const recordings = [
    {
      id: 1,
      camera: "Front Door",
      date: "Today, 10:42 AM",
      duration: "00:32",
      type: "Motion",
      thumbnail: "/placeholder.svg?height=180&width=320",
    },
    {
      id: 2,
      camera: "Back Yard",
      date: "Today, 09:15 AM",
      duration: "01:15",
      type: "Person",
      thumbnail: "/placeholder.svg?height=180&width=320",
    },
    {
      id: 3,
      camera: "Garage",
      date: "Today, 08:30 AM",
      duration: "00:45",
      type: "Motion",
      thumbnail: "/placeholder.svg?height=180&width=320",
    },
    {
      id: 4,
      camera: "Living Room",
      date: "Yesterday, 07:45 PM",
      duration: "00:28",
      type: "Person",
      thumbnail: "/placeholder.svg?height=180&width=320",
    },
    {
      id: 5,
      camera: "Front Door",
      date: "Yesterday, 06:20 PM",
      duration: "00:18",
      type: "Motion",
      thumbnail: "/placeholder.svg?height=180&width=320",
    },
    {
      id: 6,
      camera: "Back Yard",
      date: "Yesterday, 05:10 PM",
      duration: "00:52",
      type: "Vehicle",
      thumbnail: "/placeholder.svg?height=180&width=320",
    },
  ]

  return (
    <div className="space-y-6">
      <Card className="border border-gray-800 bg-gray-900/50 shadow-lg">
        <CardContent className="p-4">
          <div className="flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" className="border-gray-700 bg-gray-800 text-white hover:bg-gray-700">
                <Calendar className="mr-2 h-4 w-4" />
                Select Date
              </Button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="outline"
                    size="sm"
                    className="border-gray-700 bg-gray-800 text-white hover:bg-gray-700"
                  >
                    <Filter className="mr-2 h-4 w-4" />
                    Filter
                    <ChevronDown className="ml-2 h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56 border-gray-800 bg-gray-900 text-white">
                  <DropdownMenuItem className="focus:bg-gray-800 focus:text-white">All Recordings</DropdownMenuItem>
                  <DropdownMenuItem className="focus:bg-gray-800 focus:text-white">Motion Events</DropdownMenuItem>
                  <DropdownMenuItem className="focus:bg-gray-800 focus:text-white">Person Detected</DropdownMenuItem>
                  <DropdownMenuItem className="focus:bg-gray-800 focus:text-white">Vehicle Detected</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            <div className="flex w-full items-center gap-2 md:w-auto">
              <Select defaultValue="all-cameras">
                <SelectTrigger className="w-full border-gray-700 bg-gray-800 text-white md:w-[180px]">
                  <SelectValue placeholder="Select Camera" />
                </SelectTrigger>
                <SelectContent className="border-gray-800 bg-gray-900 text-white">
                  <SelectItem value="all-cameras">All Cameras</SelectItem>
                  <SelectItem value="front-door">Front Door</SelectItem>
                  <SelectItem value="back-yard">Back Yard</SelectItem>
                  <SelectItem value="garage">Garage</SelectItem>
                  <SelectItem value="living-room">Living Room</SelectItem>
                </SelectContent>
              </Select>

              <Tabs
                defaultValue="grid"
                className="w-auto"
                onValueChange={(value) => setViewType(value as "grid" | "list")}
              >
                <TabsList className="bg-gray-800">
                  <TabsTrigger value="grid" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="lucide lucide-grid-2x2"
                    >
                      <rect width="18" height="18" x="3" y="3" rx="2" />
                      <path d="M3 12h18" />
                      <path d="M12 3v18" />
                    </svg>
                  </TabsTrigger>
                  <TabsTrigger value="list" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="lucide lucide-list"
                    >
                      <line x1="8" x2="21" y1="6" y2="6" />
                      <line x1="8" x2="21" y1="12" y2="12" />
                      <line x1="8" x2="21" y1="18" y2="18" />
                      <line x1="3" x2="3.01" y1="6" y2="6" />
                      <line x1="3" x2="3.01" y1="12" y2="12" />
                      <line x1="3" x2="3.01" y1="18" y2="18" />
                    </svg>
                  </TabsTrigger>
                </TabsList>
              </Tabs>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="mt-6">
        <Tabs defaultValue="grid">
          <TabsContent value="grid">
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {recordings.map((recording) => (
                <Card
                  key={recording.id}
                  className="overflow-hidden border border-gray-800 bg-gray-900/50 shadow-lg transition-all hover:border-blue-600/50 hover:shadow-xl"
                >
                  <div className="relative aspect-video bg-gray-800">
                    <img
                      src={recording.thumbnail || "/placeholder.svg"}
                      alt={`Recording from ${recording.camera}`}
                      className="h-full w-full object-cover"
                    />
                    <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 transition-opacity hover:opacity-100">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-12 w-12 rounded-full bg-blue-600/80 text-white hover:bg-blue-700"
                      >
                        <Play className="h-6 w-6" />
                      </Button>
                    </div>
                    <div className="absolute bottom-2 right-2 rounded bg-black/60 px-2 py-1 text-xs text-white">
                      {recording.duration}
                    </div>
                  </div>
                  <CardContent className="p-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-medium text-white">{recording.camera}</h3>
                        <p className="text-xs text-gray-400">{recording.date}</p>
                      </div>
                      <Badge variant="outline" className="bg-blue-600/20 text-blue-400">
                        {recording.type}
                      </Badge>
                    </div>
                    <div className="mt-2 flex justify-end gap-1">
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-400 hover:text-white">
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-400 hover:text-red-500">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="list">
            <Card className="border border-gray-800 bg-gray-900/50 shadow-lg">
              <CardContent className="p-0">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-800 bg-gray-900">
                        <th className="px-4 py-3 text-left text-sm font-medium text-gray-400">Camera</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-gray-400">Date & Time</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-gray-400">Duration</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-gray-400">Type</th>
                        <th className="px-4 py-3 text-right text-sm font-medium text-gray-400">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {recordings.map((recording) => (
                        <tr key={recording.id} className="border-b border-gray-800 hover:bg-gray-800/50">
                          <td className="px-4 py-3 text-sm text-white">{recording.camera}</td>
                          <td className="px-4 py-3 text-sm text-gray-300">{recording.date}</td>
                          <td className="px-4 py-3 text-sm text-gray-300">{recording.duration}</td>
                          <td className="px-4 py-3">
                            <Badge variant="outline" className="bg-blue-600/20 text-blue-400">
                              {recording.type}
                            </Badge>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <div className="flex justify-end gap-1">
                              <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-400 hover:text-white">
                                <Play className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-400 hover:text-white">
                                <Download className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-400 hover:text-red-500">
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

