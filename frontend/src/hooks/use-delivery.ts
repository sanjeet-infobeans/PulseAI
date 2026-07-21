"use client"

import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useSprints(projectId: string) {
  return useQuery({
    queryKey: ["sprints", projectId],
    queryFn: () => api.delivery.sprints(projectId),
    enabled: !!projectId,
  })
}

export function useStories(projectId: string, sprintId?: string) {
  return useQuery({
    queryKey: ["stories", projectId, sprintId ?? "all"],
    queryFn: () => api.delivery.stories(projectId, sprintId),
    enabled: !!projectId,
  })
}
