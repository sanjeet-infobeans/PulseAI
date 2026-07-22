"use client"

import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useDependencies(projectId: string) {
  return useQuery({
    queryKey: ["dependencies", projectId],
    queryFn: () => api.dependencies.list(projectId),
    enabled: !!projectId,
  })
}

export function useDecisions(projectId: string) {
  return useQuery({
    queryKey: ["decisions", projectId],
    queryFn: () => api.decisions.get(projectId),
    enabled: !!projectId,
  })
}
