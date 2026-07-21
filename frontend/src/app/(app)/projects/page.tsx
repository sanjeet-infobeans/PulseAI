import { redirect } from "next/navigation"

// Projects are scoped under a customer; send the top-level link to the hub.
export default function ProjectsIndex() {
  redirect("/customers")
}
