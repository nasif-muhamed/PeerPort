import { Navigate, Outlet } from "react-router-dom";
import { getAccessToken } from "../../utils/tokenManager";
import AuthenticatedLayout from "../../components/Layout/AuthenticatedLayout";

const ProtectedRoute = () => {
  const token = getAccessToken()
  console.log('token:', token)
  return token ? <AuthenticatedLayout><Outlet/></AuthenticatedLayout> : <Navigate to={'/'}/>
}

export default ProtectedRoute