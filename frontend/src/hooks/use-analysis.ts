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

export function useLatestJudgeReview(projectId: string, analysisId: string | undefined) {
  return useQuery({
    queryKey: ["judge-review", projectId, analysisId],
    queryFn: () => api.analysis.latestJudge(projectId, analysisId as string),
    enabled: !!projectId && !!analysisId,
  })
}

export function useRunJudge(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (analysisId: string) => api.analysis.judge(projectId, analysisId),
    onSuccess: (data) =>
      qc.setQueryData(["judge-review", projectId, data.analysis_id], data),
  })
}
