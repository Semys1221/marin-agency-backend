import { lazy, Suspense } from 'react'
import type { FunnelStep } from '@/types'
import { Skeleton } from '@/components/ui/skeleton'

const stepComponents: Record<string, React.LazyExoticComponent<React.ComponentType<{ step: FunnelStep }>>> = {
  landing: lazy(() => import('@/components/steps/Landing')),
  qualification: lazy(() => import('@/components/steps/Qualification')),
  calendly: lazy(() => import('@/components/steps/Calendly')),
}

function DefaultStep({ step }: { step: FunnelStep }) {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold capitalize">{step.name}</h2>
      <p className="text-muted-foreground">
        Contenu à implémenter pour l'étape {step.id} : {step.name}.
      </p>
    </div>
  )
}

export function StepRenderer({ step }: { step: FunnelStep }) {
  const Component = stepComponents[step.name]

  return (
    <Suspense fallback={<Skeleton className="h-64 w-full" />}>
      {Component ? <Component step={step} /> : <DefaultStep step={step} />}
    </Suspense>
  )
}
