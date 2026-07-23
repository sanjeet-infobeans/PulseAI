"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type {
  CreateLeaveRequest,
  CreateResourceRequest,
  UpdateLeaveRequest,
  UpdateResourceRequest,
} from "@/types/api"

export function useResourceRisk(projectId: string) {
  return useQuery({
    queryKey: ["resources", projectId],
    queryFn: () => api.resources.get(projectId),
    enabled: !!projectId,
  })
}

export function useResources(projectId: string) {
  return useQuery({
    queryKey: ["resources-roster", projectId],
    queryFn: () => api.resources.getRoster(projectId),
    enabled: !!projectId,
  })
}

export function useCreateResource(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: CreateResourceRequest) => api.resources.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["resources-roster", projectId] }),
  })
}

export function useUpdateResource(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ resourceId, body }: { resourceId: string; body: UpdateResourceRequest }) =>
      api.resources.update(projectId, resourceId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["resources-roster", projectId] }),
  })
}

export function useDeleteResource(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (resourceId: string) => api.resources.remove(projectId, resourceId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["resources-roster", projectId] }),
  })
}

export function useAddLeave(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ resourceId, body }: { resourceId: string; body: CreateLeaveRequest }) =>
      api.resources.addLeave(projectId, resourceId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["resources-roster", projectId] }),
  })
}

export function useUpdateLeave(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ resourceId, leaveId, body }: { resourceId: string; leaveId: string; body: UpdateLeaveRequest }) =>
      api.resources.updateLeave(projectId, resourceId, leaveId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["resources-roster", projectId] }),
  })
}

export function useDeleteLeave(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ resourceId, leaveId }: { resourceId: string; leaveId: string }) =>
      api.resources.removeLeave(projectId, resourceId, leaveId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["resources-roster", projectId] }),
  })
}
