"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { ActionItemStatus } from "@/types/api"

export function useActionItems(projectId: string) {
  return useQuery({
    queryKey: ["action-items", projectId],
    queryFn: () => api.actionItems.get(projectId),
    enabled: !!projectId,
  })
}

export function useSetActionItemStatus(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ itemId, status }: { itemId: string; status: ActionItemStatus }) =>
      api.actionItems.setStatus(projectId, itemId, status),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["action-items", projectId] }),
  })
}
