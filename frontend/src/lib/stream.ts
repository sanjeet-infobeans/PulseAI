import { clearToken, getToken } from "@/lib/api"

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export type StreamEvent =
  | { type: "token"; value: string }
  | { type: "citations"; value: Array<{ type: string; ref: string; label: string }> }
  | { type: "error"; value: string }
  | { type: "done" }

/** POST + Server-Sent-Events reader. EventSource is GET-only, so we read the
 *  ReadableStream ourselves and parse `data:` lines. */
export async function streamSSE(
  path: string,
  body: unknown,
  handlers: {
    onEvent: (e: StreamEvent) => void
    signal?: AbortSignal
  }
): Promise<void> {
  const token = getToken()
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
    signal: handlers.signal,
  })

  if (res.status === 401) {
    clearToken()
    if (typeof window !== "undefined") window.location.href = "/login"
    throw new Error("Session expired")
  }
  if (!res.ok || !res.body) {
    const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }))
    throw new Error((err as { detail?: string }).detail ?? `HTTP ${res.status}`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ""

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const frames = buffer.split("\n\n")
    buffer = frames.pop() ?? ""
    for (const frame of frames) {
      const line = frame.split("\n").find((l) => l.startsWith("data:"))
      if (!line) continue
      const payload = line.slice(5).trim()
      if (!payload) continue
      try {
        handlers.onEvent(JSON.parse(payload) as StreamEvent)
      } catch {
        // ignore malformed frame
      }
    }
  }
}
