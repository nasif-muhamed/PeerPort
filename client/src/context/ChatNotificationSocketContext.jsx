import { useState, useEffect, useContext, createContext, useCallback } from "react";
import { useAuthTokens } from "../hooks/useAuthTokens";

const ChatNotificationSocketContext = createContext();

export const ChatNotificationSocketProvider = ({ children, endpoint }) => {
  const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || "ws://localhost:8000";
  const DEBUG_MODE = import.meta.env.VITE_APP_DEBUG === 'true';
  const { accessToken } = useAuthTokens();
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (!accessToken || !endpoint) return;

    const websocket = new WebSocket(`${WS_BASE_URL}${endpoint}?token=${accessToken}`);

    websocket.onopen = () => {
      if (DEBUG_MODE) console.log("Chat WebSocket connected");
      setWs(websocket);
    };

    websocket.onerror = (error) => {
      if (DEBUG_MODE) console.error("Chat WebSocket error:", error);
    };

    websocket.onclose = (event) => {
      if (DEBUG_MODE) console.log("Chat WebSocket disconnected", event);
      setWs(null);
    };

    return () => {
      websocket.close();
    };
  }, [accessToken, endpoint]);

  const wsSend = useCallback(
    (msg) => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(msg));
      } else {
        console.warn("WebSocket is not connected");
      }
    },
    [ws]
  );

  const wsListen = useCallback(
    (callback) => {
      if (!ws) return;
      ws.onmessage = (event) => callback(JSON.parse(event.data));
    },
    [ws]
  );

  return (
    <ChatNotificationSocketContext.Provider value={{ ws, wsSend, wsListen }}>
      {children}
    </ChatNotificationSocketContext.Provider>
  );
};

export const useWebSocket = () => useContext(ChatNotificationSocketContext);