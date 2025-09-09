import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useWebSocket } from "../../context/ChatNotificationSocketContext";
import { toast } from "sonner";
import { useAuthTokens } from "../../hooks/useAuthTokens"

const ChatEventHandler = ({ fetchRoomDetails, fetchMessages, setMessages, room, setRoom }) => {
  const DEBUG_MODE = import.meta.env.VITE_APP_DEBUG === 'true';
  const { ws, wsListen } = useWebSocket();
  const { userId } = useAuthTokens()

  useEffect(() => {
    // listen to the recieving messages.
    wsListen((data) => {
      if (DEBUG_MODE) console.log('ws listen:', data)

      if (data.type === "chat_recieved") {
        const sender = data.payload?.sender
        const message = data.payload?.message
        if (sender != userId) {
          setMessages((prev) => [
            ...prev, { ...message, msg_type: 'received', }
          ]);
        }
      }

      else if (data.type === "group_notification") {
        const messageRoomId = data.room_id;
        const subType = data.sub_type;
        const senderId = data.payload?.sender_id

        if (subType === 'joined' || subType === 'left') {
          if (senderId !== userId) {
            toast.info(data.payload.message || '');
          }
          
          if (senderId !== room.owner?.id) {
            setRoom(prev => ({
              ...prev,
              participant_count: subType === 'joined' 
                ? prev.participant_count + 1 
                : prev.participant_count - 1
            }));
          }
        }
      }
    });

  }, [wsListen, setMessages, room, setRoom]);

  useEffect(() => {
    if (!ws) return
    fetchRoomDetails()
    fetchMessages()
  }, [ws])
  
  return null;
};

export default ChatEventHandler;