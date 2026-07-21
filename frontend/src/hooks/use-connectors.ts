"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { Connector, ConnectorType } from "@/types/api"

export function useConnectors(projectId: string) {
  return useQuery({
    queryKey: ["connectors", projectId],
    queryFn: () => api.connectors.list(projectId),
    enabled: !!projectId,
  })
}

/** Poll a connector's status while a sync is running. */
export function useConnectorStatus(projectId: string, cid: string | undefined, active: boolean) {
  return useQuery({
    queryKey: ["connector-status", projectId, cid],
    queryFn: () => api.connectors.status(projectId, cid!),
    enabled: !!projectId && !!cid && active,
    refetchInterval: (query) =>
      query.state.data?.status === "syncing" ? 2000 : false,
  })
}

export function useAssignConnector(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: {
      type: ConnectorType
      mode?: "real" | "simulated"
      config: Record<string, unknown>
      secret_ref?: string | null
    }) => api.connectors.assign(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["connectors", projectId] }),
  })
}

export function useSyncConnector(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (cid: string) => api.connectors.sync(projectId, cid),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["connectors", projectId] })
    },
  })
}

export function useTestConnector(projectId: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (cid: string) => api.connectors.test(projectId, cid),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["connectors", projectId] }),
  })
}

export function jiraConnector(connectors: Connector[] | undefined): Connector | undefined {
  return connectors?.find((c) => c.type === "jira")
}
