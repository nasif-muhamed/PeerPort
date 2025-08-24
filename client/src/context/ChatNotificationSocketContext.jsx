import { useState, useEffect, useContext, createContext } from 'react'
import { useAuthTokens } from '../hooks/useAuthTokens';

const ChatNotificationSocketContext = createContext();

export const ChatNotificationSocketProvider = ({children, endpoint}) => {
  const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';
  const { accessToken } = useAuthTokens()
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (!accessToken || !endpoint) return;

    const websocket = new WebSocket(`${WS_BASE_URL}${endpoint}?token=${accessToken}`);

    websocket.onopen = () => console.log('Chat WebSocket connected with access:', accessToken);
    websocket.onerror = (error) => console.error('Chat WebSocket error:', error);
    websocket.onclose = () => console.log('Chat WebSocket disconnected');

    setWs(websocket);

    return () => websocket.close();
  }, [accessToken, endpoint]);

  return (
    <ChatNotificationSocketContext.Provider value={ws}>
      {children}
    </ChatNotificationSocketContext.Provider>
  )
}

export const useWebSocket = () => useContext(ChatNotificationSocketContext);