"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { CreateCustomerRequest, UpdateCustomerRequest } from "@/types/api"

export function useCustomers() {
  return useQuery({ queryKey: ["customers"], queryFn: api.customers.list })
}

export function useCustomer(id: string) {
  return useQuery({ queryKey: ["customer", id], queryFn: () => api.customers.get(id), enabled: !!id })
}

export function useCreateCustomer() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: CreateCustomerRequest) => api.customers.create(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["customers"] }),
  })
}

export function useUpdateCustomer(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: UpdateCustomerRequest) => api.customers.update(id, body),
    onSuccess: (data) => {
      qc.setQueryData(["customer", id], data)
      qc.invalidateQueries({ queryKey: ["customers"] })
    },
  })
}
