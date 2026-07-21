import { CustomerDetailContent } from "./customer-detail-content"

export const dynamic = "force-dynamic"

export default function CustomerDetailPage({ params }: { params: { id: string } }) {
  return <CustomerDetailContent customerId={params.id} />
}
