import { create } from 'zustand'
import type { FunnelStep } from '@/types'

export const AGENCY_STEPS: string[] = [
  'landing', 'qualification', 'calendly', 'cadre', 'profil',
  'probleme', 'objectif', 'historique', 'capacite', 'posture',
  'blocage', 'solution', 'projection', 'workflow', 'inaction-cost',
  'proposal', 'paiement', 'gift', 'contract', 'onboarding',
  'call-1', 'call-2',
]

export const ECOMMERCE_STEPS: string[] = [
  'landing', 'qualification', 'calendly', 'cadre', 'profil',
  'probleme', 'objectif', 'solution', 'proposal',
  'paiement', 'tracking',
]

interface FunnelState {
  currentStep: number
  steps: FunnelStep[]
  data: Record<string, unknown>
  offerType: 'agency' | 'ecommerce'

  setOfferType: (type: 'agency' | 'ecommerce') => void
  nextStep: () => void
  prevStep: () => void
  goToStep: (id: number) => void
  setStepData: (stepId: number, data: Record<string, unknown>) => void
  completeStep: (stepId: number) => void
  isLastStep: () => boolean
  progress: () => number
}

function buildSteps(type: 'agency' | 'ecommerce'): FunnelStep[] {
  const names = type === 'agency' ? AGENCY_STEPS : ECOMMERCE_STEPS
  return names.map((name, i) => ({
    id: i + 1,
    name,
    data: {},
    completed: false,
  }))
}

export const useFunnelStore = create<FunnelState>((set, get) => ({
  currentStep: 1,
  steps: buildSteps('agency'),
  data: {},
  offerType: 'agency',

  setOfferType: (type) => set({ offerType: type, steps: buildSteps(type), currentStep: 1 }),

  nextStep: () => {
    const { currentStep, steps } = get()
    if (currentStep < steps.length) {
      set({ currentStep: currentStep + 1 })
    }
  },

  prevStep: () => {
    const { currentStep } = get()
    if (currentStep > 1) {
      set({ currentStep: currentStep - 1 })
    }
  },

  goToStep: (id) => set({ currentStep: id }),

  setStepData: (stepId, data) => {
    const { steps } = get()
    const updated = steps.map((s) =>
      s.id === stepId ? { ...s, data: { ...s.data, ...data } } : s
    )
    set({ steps: updated })
  },

  completeStep: (stepId) => {
    const { steps } = get()
    const updated = steps.map((s) =>
      s.id === stepId ? { ...s, completed: true } : s
    )
    set({ steps: updated })
  },

  isLastStep: () => {
    const { currentStep, steps } = get()
    return currentStep >= steps.length
  },

  progress: () => {
    const { currentStep, steps } = get()
    return Math.round((currentStep / steps.length) * 100)
  },
}))
