import { Navigate, Outlet } from "react-router-dom";
import { getAccessToken } from "../../utils/tokenManager";

const GuestRoute = () => {
  const token = getAccessToken()
  return token ? <Navigate to={'/dashboard'}/> : <Outlet/>
}

export default GuestRoute
