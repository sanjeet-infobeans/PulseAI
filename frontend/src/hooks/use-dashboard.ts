"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useDashboard(projectId: string) {
  return useQuery({
    queryKey: ["dashboard", projectId],
    queryFn: () => api.dashboard.get(projectId),
    enabled: !!projectId,
  })
}

export function useComputeConfidence(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: () => api.confidence.compute(projectId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["dashboard", projectId] }),
  })
}

export function useAlignment(projectId: string) {
  return useMutation({ mutationFn: () => api.confidence.alignment(projectId) })
}
