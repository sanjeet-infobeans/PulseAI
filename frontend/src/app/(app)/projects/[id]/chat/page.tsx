import { ChatContent } from "./chat-content"

export const dynamic = "force-dynamic"

export default function ChatPage({ params }: { params: { id: string } }) {
  return <ChatContent projectId={params.id} />
}
