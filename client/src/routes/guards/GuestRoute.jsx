import { Navigate, Outlet } from "react-router-dom";

import { useAuthTokens } from "../../hooks/useAuthTokens";

const GuestRoute = () => {
  const { accessToken } = useAuthTokens()
  return accessToken ? <Navigate to={'/dashboard'}/> : <Outlet/>
}

export default GuestRoute
