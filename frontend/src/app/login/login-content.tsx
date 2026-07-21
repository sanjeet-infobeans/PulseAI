"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Gauge } from "@phosphor-icons/react"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

async function landingRoute(): Promise<string> {
  // Super admins manage the portfolio; customers go straight to their workspace.
  try {
    const me = await api.auth.me()
    if (me.role === "customer" && me.customer_id) {
      const projects = await api.projects.listByCustomer(me.customer_id)
      if (projects.length === 1) return `/projects/${projects[0].id}`
      return `/customers/${me.customer_id}`
    }
  } catch {
    /* fall through to portfolio */
  }
  return "/customers"
}

export function LoginContent() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isPending, setIsPending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setIsPending(true)
    try {
      await api.auth.login(email.trim(), password)
      router.push(await landingRoute())
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed")
    } finally {
      setIsPending(false)
    }
  }

  return (
    <div className="w-full max-w-sm">
      <div className="mb-8 flex flex-col items-center text-center">
        <div className="w-14 h-14 bg-primary flex items-center justify-center rounded-md mb-4">
          <Gauge size={30} weight="regular" className="text-white" />
        </div>
        <p className="text-charcoal text-3xl font-light tracking-tight leading-none">PulseAI</p>
        <p className="text-medium-gray text-sm mt-2">Deliver confidence · InfoBeans</p>
      </div>

      <div className="premium-card rounded-xl p-8">
        <p className="eyebrow mb-2">Sign in</p>
        <h1 className="text-headline-md text-charcoal mb-6">Welcome back</h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@infobeans.com"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {error && <p className="text-xs text-primary">{error}</p>}

          <Button type="submit" disabled={isPending || !email || !password} size="lg" className="mt-1">
            {isPending ? "Signing in…" : "Sign in"}
          </Button>
        </form>
      </div>
    </div>
  )
}
