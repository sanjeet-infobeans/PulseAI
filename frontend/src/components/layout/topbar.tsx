"use client"

import { MagnifyingGlass, Sparkle, Bell } from "@phosphor-icons/react"

export function Topbar({ title }: { title?: string }) {
  return (
    <header className="h-20 fixed top-0 left-[280px] right-0 z-40 bg-surface/95 backdrop-blur-md border-b border-light-gray flex justify-between items-center px-margin-desktop">
      <div className="flex items-center gap-8">
        {title ? (
          <h2 className="text-headline-md text-charcoal">{title}</h2>
        ) : (
          <div className="relative">
            <MagnifyingGlass
              size={16}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-medium-gray"
            />
            <input
              type="text"
              placeholder="Search portfolio..."
              className="bg-background border-none rounded-sm pl-10 pr-4 py-2 text-sm w-80 focus:ring-1 focus:ring-primary/30 focus:outline-none placeholder:text-medium-gray/50"
            />
          </div>
        )}
      </div>
      <div className="flex items-center gap-6">
        <button className="flex items-center gap-2 px-4 py-2 bg-primary/5 text-primary rounded-sm text-label-md hover:bg-primary/10 transition-colors">
          <Sparkle size={16} weight="regular" />
          Generate insights
        </button>
        <div className="h-6 w-px bg-light-gray" />
        <button className="text-medium-gray hover:text-charcoal transition-colors relative" aria-label="Notifications">
          <Bell size={22} weight="regular" />
          <span className="absolute top-0 right-0 w-2 h-2 bg-primary rounded-full" />
        </button>
        <div className="w-10 h-10 rounded-full bg-light-gray flex items-center justify-center text-xs text-medium-gray">
          IB
        </div>
      </div>
    </header>
  )
}
