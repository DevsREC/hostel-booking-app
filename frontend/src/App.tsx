import { Route, Routes } from 'react-router'
import { MainLayout } from './components/global/main-layout'
import Login from './app/auth/login/login'
import PageNotFound from './app/page-not-found/page'
import Dashboard from './app/main/page'
import AuthLayout from './app/auth/layout'
import { ProtectedRoute, PublicOnlyRoute } from './components/auth/protected-route'
import DashboardLayout from './app/main/layout'
import ForgotPassword from './app/auth/forgot-password/page'
import { fetchCSRFToken, setupCSRF } from './utils/csrf'
import { useEffect } from 'react'
import ReactGA from 'react-ga4'
import SpecialFormPage from './app/main/special-form/page';

function App() {

  useEffect(() => {
    setupCSRF();
    fetchCSRFToken().catch(error => {
      console.error('Failed to fetch CSRF token:', error);
    });
  }, []);

  useEffect(() => {
    ReactGA.send({
      hitType: "Home Page",
      page: "/",
      title: "Hostel Booking App",
    });
  }, []);

  return (
    <MainLayout>
      <Routes>
        {/* Public routes */}
        {/* <Route path="/landing" element={<Landing />} /> */}

        <Route path="/auth" element={<AuthLayout />}>
          <Route path="login" element={
            <PublicOnlyRoute>
              <Login />
            </PublicOnlyRoute>
          } />
          <Route path="forgot-password" element={
            <PublicOnlyRoute>
              <ForgotPassword />
            </PublicOnlyRoute>
          } />
        </Route>

        {/* Special form route at top level */}

        <Route element={<DashboardLayout />}>
          <Route path="/*" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
        </Route>

        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </MainLayout>
  )
}

export default App

