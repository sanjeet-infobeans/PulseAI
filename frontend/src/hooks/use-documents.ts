"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useDocuments(projectId: string) {
  return useQuery({
    queryKey: ["documents", projectId],
    queryFn: () => api.documents.list(projectId),
    enabled: !!projectId,
    // Poll while any document is still processing.
    refetchInterval: (query) => {
      const docs = query.state.data
      const pending = docs?.some((d) =>
        ["uploaded", "parsing", "analyzing"].includes(d.status)
      )
      return pending ? 2000 : false
    },
  })
}

export function useUploadDocument(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ file, docType }: { file: File; docType: string }) =>
      api.documents.upload(projectId, file, docType),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["documents", projectId] }),
  })
}

export function useDeleteDocument(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (docId: string) => api.documents.remove(docId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["documents", projectId] }),
  })
}
