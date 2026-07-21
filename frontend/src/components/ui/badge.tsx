import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-normal rounded-sm transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary/5 text-primary",
        neutral: "bg-light-gray text-medium-gray",
        // Health / confidence bands (semantic, separate from the accent)
        "health-good": "bg-good/10 text-good",
        "health-warn": "bg-warn/10 text-warn",
        "health-risk": "bg-primary/10 text-primary",
        // Risk severity
        "severity-high": "bg-primary/10 text-primary",
        "severity-med": "bg-light-gray text-charcoal",
        "severity-low": "bg-light-gray text-medium-gray",
        // Roadmap / simulated screens
        future: "border border-charcoal/30 text-medium-gray",
      },
    },
    defaultVariants: { variant: "default" },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
