import { useFunnelStore } from '@/stores/funnel'
import type { FunnelStep } from '@/types'
import { Badge } from '@/components/ui/badge'

export default function Calendly({ step }: { step: FunnelStep }) {
  const { completeStep } = useFunnelStore()

  return (
    <div className="space-y-6">
      <Badge variant="secondary" className="mb-2">Étape 3</Badge>
      <h2 className="text-2xl font-semibold">Choisissez votre créneau</h2>
      <p className="text-muted-foreground">
        Réservez un appel de 30 minutes avec notre équipe.
      </p>
      <div className="flex h-64 items-center justify-center rounded-lg border bg-secondary/50">
        <p className="text-muted-foreground">
          Calendly embed — disponible après intégration
        </p>
      </div>
    </div>
  )
}
