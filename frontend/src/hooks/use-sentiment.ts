"use client"

import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useSentiment(projectId: string) {
  return useQuery({
    queryKey: ["sentiment", projectId],
    queryFn: () => api.sentiment.get(projectId),
    enabled: !!projectId,
  })
}
