import { useFunnelStore } from '@/stores/funnel'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { motion, AnimatePresence } from 'framer-motion'
import { StepRenderer } from '@/components/steps/StepRenderer'

export default function FunnelFlow() {
  const { currentStep, steps, nextStep, prevStep, progress, isLastStep } = useFunnelStore()
  const step = steps.find((s) => s.id === currentStep)

  return (
    <div className="min-h-screen bg-background">
      <div className="mx-auto max-w-2xl px-4 py-8">
        <Progress value={progress()} className="mb-8 h-2" />

        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Card className="backdrop-blur-sm bg-card/80 shadow-lg">
              <CardContent className="p-8">
                {step ? (
                  <StepRenderer step={step} />
                ) : (
                  <p className="text-center text-muted-foreground">Step not found</p>
                )}

                <div className="mt-8 flex justify-between">
                  <Button
                    variant="outline"
                    onClick={prevStep}
                    disabled={currentStep === 1}
                  >
                    Précédent
                  </Button>
                  <Button onClick={nextStep}>
                    {isLastStep() ? 'Terminer' : 'Suivant'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </AnimatePresence>

        <p className="mt-4 text-center text-sm text-muted-foreground">
          Étape {currentStep} sur {steps.length}
        </p>
      </div>
    </div>
  )
}
