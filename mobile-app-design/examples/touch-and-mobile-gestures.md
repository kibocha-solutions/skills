# Mobile and Touch Gesture Patterns

This document provides production-grade implementation patterns for mobile touch interactions, sheet gestures, swipeable list actions, and adaptive master-detail layouts.

## 1. Expandable Bottom Sheet with Drag Handle

```html
<!-- Bottom Sheet Container with Drag Handle and Scrim -->
<div class="fixed inset-0 z-50 flex flex-col justify-end bg-black/40 backdrop-blur-sm transition-opacity">
  <div 
    class="w-full bg-white dark:bg-zinc-900 rounded-t-2xl shadow-xl flex flex-col max-h-[90vh] pb-[env(safe-area-inset-bottom,16px)] animate-sheet-slide-up"
    role="dialog"
    aria-modal="true"
    aria-labelledby="sheet-title">
    
    <!-- Tactile Drag Handle -->
    <div class="w-full flex justify-center py-3 cursor-grab active:cursor-grabbing touch-none">
      <div class="w-10 h-1 bg-zinc-300 dark:bg-zinc-700 rounded-full"></div>
    </div>

    <!-- Sheet Header -->
    <div class="px-6 pb-4 border-b border-zinc-100 dark:border-zinc-800 flex items-center justify-between">
      <h2 id="sheet-title" class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
        Payment Methods
      </h2>
      <button 
        type="button"
        class="w-8 h-8 flex items-center justify-center rounded-full text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800 active:scale-95 transition"
        aria-label="Close sheet">
        ✕
      </button>
    </div>

    <!-- Scrollable Sheet Content -->
    <div class="px-6 py-4 overflow-y-auto overscroll-contain flex flex-col gap-3">
      <button 
        type="button" 
        class="w-full p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 flex items-center justify-between active:scale-[0.98] transition-transform">
        <span class="font-medium text-sm text-zinc-900 dark:text-zinc-100">Apple Pay</span>
        <span class="text-xs text-blue-600 font-semibold">Connected</span>
      </button>
      <button 
        type="button" 
        class="w-full p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 flex items-center justify-between active:scale-[0.98] transition-transform">
        <span class="font-medium text-sm text-zinc-900 dark:text-zinc-100">Credit or Debit Card</span>
        <span class="text-xs text-zinc-400">Default</span>
      </button>
    </div>
  </div>
</div>
```

---

## 2. Swipeable List Item with Action Reveal

```html
<!-- Swipeable Row Container -->
<div class="relative overflow-hidden rounded-lg bg-red-600">
  <!-- Revealed Under-Surface Actions -->
  <div class="absolute inset-y-0 right-0 flex items-center justify-end px-6 text-white font-medium text-sm">
    Delete
  </div>

  <!-- Swipeable Foreground Card -->
  <div 
    class="relative bg-white dark:bg-zinc-900 p-4 border border-zinc-200 dark:border-zinc-800 rounded-lg flex items-center justify-between transition-transform touch-pan-y"
    style="transform: translateX(0px);">
    <div class="flex flex-col gap-0.5">
      <span class="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Weekly Performance Report</span>
      <span class="text-xs text-zinc-500">Updated 2 hours ago</span>
    </div>
    <span class="text-xs font-mono text-zinc-400">1.4 MB</span>
  </div>
</div>
```

---

## 3. Tablet Landscape: Master-Detail Layout

```html
<!-- Master-Detail Dual Pane for Tablet Landscape -->
<div class="hidden md:flex h-screen w-full bg-zinc-50 dark:bg-zinc-950 overflow-hidden">
  
  <!-- Left Master Pane (Fixed Width, Scrollable List) -->
  <aside class="w-80 border-r border-zinc-200 dark:border-zinc-800 flex flex-col bg-white dark:bg-zinc-900">
    <div class="p-4 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between">
      <h1 class="text-base font-bold text-zinc-900 dark:text-zinc-100">Inbox</h1>
      <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300">
        12 new
      </span>
    </div>
    <div class="flex-1 overflow-y-auto divide-y divide-zinc-100 dark:divide-zinc-800">
      <button class="w-full text-left p-4 bg-blue-50/50 dark:bg-blue-950/20 flex flex-col gap-1 border-l-4 border-blue-600">
        <span class="text-sm font-medium text-zinc-900 dark:text-zinc-100">Design System Tokens</span>
        <span class="text-xs text-zinc-500 line-clamp-2">New spring physics curves calibrated for mobile sheets...</span>
      </button>
      <button class="w-full text-left p-4 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 flex flex-col gap-1">
        <span class="text-sm font-medium text-zinc-900 dark:text-zinc-100">Release Checklist</span>
        <span class="text-xs text-zinc-500 line-clamp-2">All acceptance criteria verified against exact artifacts...</span>
      </button>
    </div>
  </aside>

  <!-- Right Detail Pane (Fluid Width, Deep Context) -->
  <main class="flex-1 flex flex-col bg-white dark:bg-zinc-900 overflow-y-auto p-8">
    <div class="max-w-prose flex flex-col gap-4">
      <h2 class="text-2xl font-bold text-zinc-900 dark:text-zinc-100">Design System Tokens</h2>
      <p class="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
        The revised interaction standards enforce frequency-based duration brackets, ensuring high-frequency actions register within 100ms to 150ms while sheet transitions use calibrated spring damping.
      </p>
    </div>
  </main>
</div>
```
