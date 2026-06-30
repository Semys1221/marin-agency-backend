import { useFunnelStore } from '@/stores/funnel'
import type { FunnelStep } from '@/types'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import config from '@/config/client'

const mockOffer = {
  name: 'Offre Principale',
  price: '2 500 €',
  guarantee: '10 ventes ou on continue',
  duration: '90 jours',
}

export default function Landing({ step }: { step: FunnelStep }) {
  const { completeStep, setStepData } = useFunnelStore()

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Badge variant="secondary" className="mb-2">Étape 1</Badge>
        <h1 className="text-3xl font-bold">
          Transformez vos prospects en clients avec {config.name}
        </h1>
        <p className="text-lg text-muted-foreground">
          L'agence qui construit votre pipeline de vente clé en main — de la prospection à la signature
        </p>
      </div>

      <Separator />

      <div className="grid gap-4 rounded-lg border p-6">
        <h2 className="text-xl font-semibold">Notre offre</h2>
        <div className="space-y-2">
          <p><strong>{mockOffer.name}</strong></p>
          <p>Prix : {mockOffer.price}</p>
          <p>Garantie : {mockOffer.guarantee}</p>
          <p>Durée : {mockOffer.duration}</p>
        </div>
      </div>

      <div className="space-y-2 rounded-lg bg-secondary p-4">
        <h3 className="font-medium">Comment ça marche</h3>
        <ol className="list-inside list-decimal space-y-1 text-sm text-muted-foreground">
          <li>Qualification SIRET instantanée</li>
          <li>Call découverte de 30 min</li>
          <li>Setup 15 jours</li>
          <li>Accompagnement 90 jours</li>
        </ol>
      </div>
    </div>
  )
}
