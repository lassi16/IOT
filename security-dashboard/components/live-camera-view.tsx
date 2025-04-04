'use client';

import { useState } from 'react';
import { Camera, Maximize2, Mic, MicOff, Volume2, VolumeX } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function LiveCameraView() {
    const [isMuted, setIsMuted] = useState(true);
    const [isMicOn, setIsMicOn] = useState(false);

    const cameras = [
        { id: 'front-door', name: 'Front Door' },
        { id: 'back-yard', name: 'Back Yard' },
        { id: 'garage', name: 'Garage' },
        { id: 'living-room', name: 'Living Room' },
    ];

    return (
        <div className="space-y-6">
            <Tabs defaultValue="front-door" className="w-full">
                <TabsList className="mb-4 grid w-full grid-cols-2 bg-gray-800 md:grid-cols-4">
                    {cameras.map((camera) => (
                        <TabsTrigger
                            key={camera.id}
                            value={camera.id}
                            className="data-[state=active]:bg-blue-600 data-[state=active]:text-white"
                        >
                            {camera.name}
                        </TabsTrigger>
                    ))}
                </TabsList>

                {cameras.map((camera) => (
                    <TabsContent key={camera.id} value={camera.id}>
                        <Card className="border border-gray-800 bg-gray-900/50 shadow-lg">
                            <CardContent className="p-0">
                                <div className="relative">
                                    <div className="aspect-video bg-gray-800">
                                        <div className="flex h-full flex-col items-center justify-center">
                                            <div className="mb-4 animate-pulse rounded-full bg-blue-600/20 p-6">
                                                <Camera className="h-12 w-12 text-blue-500" />
                                            </div>
                                            <p className="text-lg font-medium text-white">{camera.name} Camera</p>
                                            <p className="text-sm text-gray-400">Live Feed</p>
                                            <div className="mt-4 flex items-center space-x-1">
                                                <span className="h-2 w-2 animate-pulse rounded-full bg-red-500"></span>
                                                <span className="text-xs text-gray-400">LIVE</span>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Camera controls */}
                                    <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-gray-900 p-4">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center space-x-2">
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-8 w-8 rounded-full bg-gray-800/80 text-white hover:bg-gray-700"
                                                    onClick={() => setIsMuted(!isMuted)}
                                                >
                                                    {isMuted ? (
                                                        <VolumeX className="h-4 w-4" />
                                                    ) : (
                                                        <Volume2 className="h-4 w-4" />
                                                    )}
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-8 w-8 rounded-full bg-gray-800/80 text-white hover:bg-gray-700"
                                                    onClick={() => setIsMicOn(!isMicOn)}
                                                >
                                                    {isMicOn ? (
                                                        <Mic className="h-4 w-4" />
                                                    ) : (
                                                        <MicOff className="h-4 w-4" />
                                                    )}
                                                </Button>
                                            </div>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8 rounded-full bg-gray-800/80 text-white hover:bg-gray-700"
                                            >
                                                <Maximize2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        <div className="mt-6 grid gap-6 md:grid-cols-2">
                            <Card className="border border-gray-800 bg-gray-900/50 shadow-lg">
                                <CardContent className="p-4">
                                    <h3 className="mb-2 text-lg font-medium text-white">Camera Details</h3>
                                    <div className="space-y-2 text-sm text-gray-400">
                                        <div className="flex justify-between">
                                            <span>Status:</span>
                                            <span className="text-green-500">Online</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span>Resolution:</span>
                                            <span>1080p HD</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span>Last Motion:</span>
                                            <span>2 minutes ago</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span>Battery:</span>
                                            <span>87%</span>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>

                            <Card className="border border-gray-800 bg-gray-900/50 shadow-lg">
                                <CardContent className="p-4">
                                    <h3 className="mb-2 text-lg font-medium text-white">Recent Activity</h3>
                                    <div className="space-y-3">
                                        {[
                                            { time: '10:42 AM', event: 'Motion detected' },
                                            { time: '09:15 AM', event: 'Person detected' },
                                            { time: '08:30 AM', event: 'Recording started' },
                                            { time: '07:45 AM', event: 'Motion detected' },
                                        ].map((activity, i) => (
                                            <div
                                                key={i}
                                                className="flex items-center justify-between border-b border-gray-800 pb-2 text-sm"
                                            >
                                                <span className="text-gray-400">{activity.time}</span>
                                                <span className="text-white">{activity.event}</span>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </TabsContent>
                ))}
            </Tabs>
        </div>
    );
}
