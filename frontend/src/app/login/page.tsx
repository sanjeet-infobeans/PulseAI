import { LoginContent } from "./login-content"

export const dynamic = "force-dynamic"

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6">
      <LoginContent />
    </div>
  )
}
