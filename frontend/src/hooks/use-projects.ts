"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { CreateProjectRequest } from "@/types/api"

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
