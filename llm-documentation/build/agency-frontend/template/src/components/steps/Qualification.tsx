import { useState } from 'react'
import { useFunnelStore } from '@/stores/funnel'
import type { FunnelStep } from '@/types'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'

export default function Qualification({ step }: { step: FunnelStep }) {
  const [siret, setSiret] = useState('')
  const [status, setStatus] = useState<'idle' | 'valid' | 'invalid'>('idle')
  const { setStepData, completeStep } = useFunnelStore()

  function handleCheck() {
    if (siret.length === 14) {
      setStatus('valid')
      setStepData(step.id, { siret, valid: true })
      completeStep(step.id)
    } else {
      setStatus('invalid')
    }
  }

  return (
    <div className="space-y-6">
      <Badge variant="secondary" className="mb-2">Étape 2</Badge>
      <h2 className="text-2xl font-semibold">Vérifions votre éligibilité</h2>
      <p className="text-muted-foreground">
        Avant de passer un appel, tous vos prospects seront vérifiés en SIRET instantanément.
      </p>

      <div className="space-y-2">
        <Label htmlFor="siret">Numéro SIRET</Label>
        <Input
          id="siret"
          placeholder="14 chiffres"
          value={siret}
          onChange={(e) => setSiret(e.target.value)}
          maxLength={14}
        />
      </div>

      {status === 'valid' && (
        <p className="text-sm text-green-600">SIRET valide — vous pouvez continuer</p>
      )}
      {status === 'invalid' && (
        <p className="text-sm text-destructive">SIRET invalide. Vérifiez le numéro.</p>
      )}
    </div>
  )
}
