import { Navigate, Outlet } from "react-router-dom";

import { useAuthTokens } from "../../hooks/useAuthTokens";

const ProtectedRoute = () => {
  const { accessToken } = useAuthTokens()
  return accessToken ? <Outlet/> : <Navigate to={'/'}/>
}

export default ProtectedRoute