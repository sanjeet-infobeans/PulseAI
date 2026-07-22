import type {
  AlignmentData,
  Analysis,
  AnalysisKind,
  ChatMessageT,
  ChatSessionT,
  Connector,
  ConnectorType,
  ConfidenceData,
  CreateCustomerRequest,
  CreateProjectRequest,
  Customer,
  DashboardData,
  DocumentT,
  MeOut,
  Project,
  ResourcesData,
  Sprint,
  Story,
  TokenOut,
} from "@/types/api"

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
const TOKEN_KEY = "pulse_token"

export function getToken(): string {
  if (typeof window === "undefined") return ""
  return localStorage.getItem(TOKEN_KEY) ?? ""
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getToken()
  const res = await fetch(`${BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers,
    },
    ...init,
  })

  if (res.status === 401) {
    if (typeof window !== "undefined") {
      clearToken()
      window.location.href = "/login"
    }
    throw new Error("Session expired")
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }))
    throw new Error((err as { detail?: string }).detail ?? `HTTP ${res.status}`)
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

export const api = {
  auth: {
    login: async (email: string, password: string): Promise<void> => {
      const res = await fetch(`${BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }))
        throw new Error((err as { detail?: string }).detail ?? "Login failed")
      }
      const { token } = (await res.json()) as TokenOut
      setToken(token)
    },

    me: () => apiFetch<MeOut>("/auth/me"),

    changePassword: (current_password: string, new_password: string) =>
      apiFetch<void>("/auth/me/password", {
        method: "PUT",
        body: JSON.stringify({ current_password, new_password }),
      }),
  },

  customers: {
    list: () => apiFetch<Customer[]>("/customers"),
    get: (id: string) => apiFetch<Customer>(`/customers/${id}`),
    create: (body: CreateCustomerRequest) =>
      apiFetch<Customer>("/customers", { method: "POST", body: JSON.stringify(body) }),
  },

  projects: {
    listByCustomer: (customerId: string) =>
      apiFetch<Project[]>(`/customers/${customerId}/projects`),
    get: (id: string) => apiFetch<Project>(`/projects/${id}`),
    create: (customerId: string, body: CreateProjectRequest) =>
      apiFetch<Project>(`/customers/${customerId}/projects`, {
        method: "POST",
        body: JSON.stringify(body),
      }),
  },

  connectors: {
    list: (projectId: string) =>
      apiFetch<Connector[]>(`/projects/${projectId}/connectors`),
    assign: (
      projectId: string,
      body: { type: ConnectorType; mode?: "real" | "simulated"; config: Record<string, unknown>; secret_ref?: string | null }
    ) =>
      apiFetch<Connector>(`/projects/${projectId}/connectors`, {
        method: "POST",
        body: JSON.stringify(body),
      }),
    test: (projectId: string, cid: string) =>
      apiFetch<{ status: string }>(`/projects/${projectId}/connectors/${cid}/test`, {
        method: "POST",
      }),
    sync: (projectId: string, cid: string) =>
      apiFetch<{ status: string; connector_id: string }>(
        `/projects/${projectId}/connectors/${cid}/sync`,
        { method: "POST" }
      ),
    status: (projectId: string, cid: string) =>
      apiFetch<Connector>(`/projects/${projectId}/connectors/${cid}/status`),
  },

  delivery: {
    sprints: (projectId: string) =>
      apiFetch<Sprint[]>(`/projects/${projectId}/sprints`),
    stories: (projectId: string, sprintId?: string) =>
      apiFetch<Story[]>(
        `/projects/${projectId}/stories${sprintId ? `?sprint_id=${sprintId}` : ""}`
      ),
  },

  analysis: {
    run: (projectId: string, kind: AnalysisKind, sprintId?: string) =>
      apiFetch<Analysis>(
        `/projects/${projectId}/analysis/${kind}${sprintId ? `?sprint_id=${sprintId}` : ""}`,
        { method: "POST" }
      ),
    latest: (projectId: string, kind: AnalysisKind) =>
      apiFetch<Analysis | null>(`/projects/${projectId}/analysis/${kind}`),
  },

  chat: {
    sessions: (projectId: string) =>
      apiFetch<ChatSessionT[]>(`/projects/${projectId}/chat/sessions`),
    createSession: (projectId: string, title = "New chat") =>
      apiFetch<ChatSessionT>(`/projects/${projectId}/chat/sessions`, {
        method: "POST",
        body: JSON.stringify({ title }),
      }),
    messages: (projectId: string, sid: string) =>
      apiFetch<ChatMessageT[]>(`/projects/${projectId}/chat/sessions/${sid}/messages`),
  },

  dashboard: {
    get: (projectId: string) => apiFetch<DashboardData>(`/projects/${projectId}/dashboard`),
  },

  resources: {
    get: (projectId: string) => apiFetch<ResourcesData>(`/projects/${projectId}/resources`),
  },

  confidence: {
    latest: (projectId: string) =>
      apiFetch<ConfidenceData | null>(`/projects/${projectId}/confidence`),
    compute: (projectId: string) =>
      apiFetch<ConfidenceData>(`/projects/${projectId}/confidence/compute`, { method: "POST" }),
    alignment: (projectId: string) =>
      apiFetch<AlignmentData>(`/projects/${projectId}/alignment`, { method: "POST" }),
  },

  documents: {
    list: (projectId: string) => apiFetch<DocumentT[]>(`/projects/${projectId}/documents`),
    get: (docId: string) => apiFetch<DocumentT>(`/documents/${docId}`),
    upload: async (projectId: string, file: File, docType: string): Promise<DocumentT> => {
      const token = getToken()
      const form = new FormData()
      form.append("file", file)
      form.append("doc_type", docType)
      const res = await fetch(`${BASE}/projects/${projectId}/documents`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: form,
      })
      if (res.status === 401) {
        clearToken()
        if (typeof window !== "undefined") window.location.href = "/login"
        throw new Error("Session expired")
      }
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }))
        throw new Error((err as { detail?: string }).detail ?? `HTTP ${res.status}`)
      }
      return res.json() as Promise<DocumentT>
    },
    remove: (docId: string) => apiFetch<void>(`/documents/${docId}`, { method: "DELETE" }),
  },
}
