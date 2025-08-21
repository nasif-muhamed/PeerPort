import { Navigate, Outlet } from "react-router-dom";

import { useAuthTokens } from "../../hooks/useAuthTokens";
import AuthenticatedLayout from "../../components/Layout/AuthenticatedLayout";

const ProtectedRoute = () => {
  const { accessToken } = useAuthTokens()
  return accessToken ? <AuthenticatedLayout><Outlet/></AuthenticatedLayout> : <Navigate to={'/'}/>
}

export default ProtectedRoute