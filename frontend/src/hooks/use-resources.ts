"use client"

import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useResources(projectId: string) {
  return useQuery({
    queryKey: ["resources", projectId],
    queryFn: () => api.resources.get(projectId),
    enabled: !!projectId,
  })
}
