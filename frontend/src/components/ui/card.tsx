import * as React from "react"
import { cn } from "@/lib/utils"

// Signature "premium-card": white, hairline border, soft shadow, near-square corners.
const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("premium-card rounded-xl", className)}
      {...props}
    />
  )
)
Card.displayName = "Card"

const CardEyebrow = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("eyebrow", className)} {...props} />
  )
)
CardEyebrow.displayName = "CardEyebrow"

const CardTitle = React.forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("text-headline-md text-charcoal leading-tight", className)} {...props} />
  )
)
CardTitle.displayName = "CardTitle"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-8", className)} {...props} />
  )
)
CardContent.displayName = "CardContent"

export { Card, CardEyebrow, CardTitle, CardContent }
