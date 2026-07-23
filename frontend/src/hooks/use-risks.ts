"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { RiskStatus } from "@/types/api"

export function useRisks(projectId: string) {
  return useQuery({
    queryKey: ["risks", projectId],
    queryFn: () => api.risks.list(projectId),
    enabled: !!projectId,
  })
}

export function useScanRisks(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: () => api.risks.scan(projectId),
    onSuccess: (data) => qc.setQueryData(["risks", projectId], data),
  })
}

export function useSetRiskStatus(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ riskId, status }: { riskId: string; status: RiskStatus }) =>
      api.risks.setStatus(projectId, riskId, status),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["risks", projectId] }),
  })
}
