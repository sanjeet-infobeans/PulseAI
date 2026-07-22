"use client"

import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useResourceRisk(projectId: string) {
  return useQuery({
    queryKey: ["resources", projectId],
    queryFn: () => api.resources.get(projectId),
    enabled: !!projectId,
  })
}
