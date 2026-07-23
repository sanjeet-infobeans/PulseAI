"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { CreateProjectRequest, UpdateProjectRequest } from "@/types/api"

export function useProjects(customerId: string) {
  return useQuery({
    queryKey: ["projects", customerId],
    queryFn: () => api.projects.listByCustomer(customerId),
    enabled: !!customerId,
  })
}

export function useProject(id: string) {
  return useQuery({
    queryKey: ["project", id],
    queryFn: () => api.projects.get(id),
    enabled: !!id,
  })
}

export function useCreateProject(customerId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: CreateProjectRequest) => api.projects.create(customerId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["projects", customerId] }),
  })
}

export function useUpdateProject(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: UpdateProjectRequest) => api.projects.update(projectId, body),
    onSuccess: (data) => {
      qc.setQueryData(["project", projectId], data)
      qc.invalidateQueries({ queryKey: ["projects", data.customer_id] })
    },
  })
}

export function useProjectOutcome(projectId: string) {
  return useQuery({
    queryKey: ["project-outcome", projectId],
    queryFn: () => api.projects.getOutcome(projectId),
    enabled: !!projectId,
  })
}

export function useMarkProjectOutcome(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (deliveredOnTime: boolean) => api.projects.markOutcome(projectId, deliveredOnTime),
    onSuccess: (data) => qc.setQueryData(["project-outcome", projectId], data),
  })
}
