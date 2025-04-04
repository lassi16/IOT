import LoginForm from "@/components/login-form"

export default function Home() {
  // In a real app, you would check if the user is authenticated
  // For demo purposes, we'll just show the login page
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-gray-900 to-gray-950">
      <div className="w-full max-w-md px-4">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-white">SecureView</h1>
          <p className="mt-2 text-gray-400">Access your security system</p>
        </div>
        <LoginForm />
      </div>
    </div>
  )
}

