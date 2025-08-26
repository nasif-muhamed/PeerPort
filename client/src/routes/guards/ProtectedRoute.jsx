import { Navigate, Outlet } from "react-router-dom";

import { useAuthTokens } from "../../hooks/useAuthTokens";
import { ChatNotificationSocketProvider } from '../../context/ChatNotificationSocketContext'; 

const ProtectedRoute = () => {
  const { accessToken } = useAuthTokens()
  return accessToken ? <ChatNotificationSocketProvider endpoint={'/ws/'}><Outlet/></ChatNotificationSocketProvider> : <Navigate to={'/'}/>
}

export default ProtectedRoute