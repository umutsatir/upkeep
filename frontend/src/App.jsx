// OWNER: MEMBER-1
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import Layout from './components/Layout.jsx'

import Dashboard       from './pages/Dashboard.jsx'
import Login           from './pages/auth/Login.jsx'
import Register        from './pages/auth/Register.jsx'

import WorkOrderList   from './pages/workOrders/WorkOrderList.jsx'
import WorkOrderDetail from './pages/workOrders/WorkOrderDetail.jsx'
import WorkOrderForm   from './pages/workOrders/WorkOrderForm.jsx'

import AssetList       from './pages/assets/AssetList.jsx'
import AssetDetail     from './pages/assets/AssetDetail.jsx'
import AssetForm       from './pages/assets/AssetForm.jsx'

import MaintenanceList   from './pages/maintenance/MaintenanceList.jsx'
import MaintenanceDetail from './pages/maintenance/MaintenanceDetail.jsx'
import MaintenanceForm   from './pages/maintenance/MaintenanceForm.jsx'

import InventoryList   from './pages/inventory/InventoryList.jsx'
import InventoryDetail from './pages/inventory/InventoryDetail.jsx'
import InventoryForm   from './pages/inventory/InventoryForm.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login"    element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected routes — all wrapped in sidebar Layout */}
          <Route
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route path="/"  element={<Dashboard />} />

            <Route path="/work-orders"         element={<WorkOrderList />} />
            <Route path="/work-orders/new"      element={<WorkOrderForm />} />
            <Route path="/work-orders/:id"      element={<WorkOrderDetail />} />
            <Route path="/work-orders/:id/edit" element={<WorkOrderForm />} />

            <Route path="/assets"         element={<AssetList />} />
            <Route path="/assets/new"      element={<AssetForm />} />
            <Route path="/assets/:id"      element={<AssetDetail />} />
            <Route path="/assets/:id/edit" element={<AssetForm />} />

            <Route path="/maintenance"          element={<MaintenanceList />} />
            <Route path="/maintenance/new"       element={<MaintenanceForm />} />
            <Route path="/maintenance/:id"       element={<MaintenanceDetail />} />
            <Route path="/maintenance/:id/edit"  element={<MaintenanceForm />} />

            <Route path="/inventory"          element={<InventoryList />} />
            <Route path="/inventory/new"       element={<InventoryForm />} />
            <Route path="/inventory/:id"       element={<InventoryDetail />} />
            <Route path="/inventory/:id/edit"  element={<InventoryForm />} />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
