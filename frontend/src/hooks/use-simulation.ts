"use client"

import { useMutation } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useRunSimulation(projectId: string) {
  return useMutation({
    mutationFn: (scenarioText: string) => api.simulation.run(projectId, scenarioText),
  })
}
