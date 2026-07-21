"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { AnalysisKind } from "@/types/api"

export function useLatestAnalysis(projectId: string, kind: AnalysisKind) {
  return useQuery({
    queryKey: ["analysis", projectId, kind],
    queryFn: () => api.analysis.latest(projectId, kind),
    enabled: !!projectId,
  })
}

export function useRunAnalysis(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ kind, sprintId }: { kind: AnalysisKind; sprintId?: string }) =>
      api.analysis.run(projectId, kind, sprintId),
    onSuccess: (data) =>
      qc.setQueryData(["analysis", projectId, data.kind], data),
  })
}
