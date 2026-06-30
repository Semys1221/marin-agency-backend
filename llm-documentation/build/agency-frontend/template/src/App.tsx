import { BrowserRouter, Routes, Route } from 'react-router-dom'
import FunnelFlow from '@/components/FunnelFlow'
import config from '@/config/client'
import { useFunnelStore } from '@/stores/funnel'
import { useEffect } from 'react'

function AppInner() {
  const { setOfferType } = useFunnelStore()

  useEffect(() => {
    setOfferType(config.offerType)
  }, [setOfferType])

  return (
    <Routes>
      <Route path="/*" element={<FunnelFlow />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AppInner />
    </BrowserRouter>
  )
}
