import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useWebSocket } from "../../context/ChatNotificationSocketContext";
import { toast } from "sonner";
import { useAuthTokens } from "../../hooks/useAuthTokens"
  
const ChatEventHandler = ({ roomId, setMessages, fetchRoomDetails, fetchMessages }) => {
  const DEBUG_MODE = import.meta.env.VITE_APP_DEBUG === 'true';
  const { wsSend, wsListen } = useWebSocket();
  const { userId, username } = useAuthTokens()
  const navigate = useNavigate();

  // join room
  useEffect(() => {
    if (!wsSend || !roomId) return;

    wsSend({
      type: "join_room",
      room_id: roomId,
      payload: {},
    });
  }, [wsSend, roomId]);

  useEffect(() => {
    if (!wsListen) return;

    // listen to the recieving messages.
    wsListen((data) => {
      if (DEBUG_MODE) console.log('ws listen:', data)
      if (data.type === "chat_recieved") {
        const sender = data.payload?.sender
        const message = data.payload?.message
        const messageRoomId = data.room_id
        if (messageRoomId == roomId){
          if (sender == userId) {
            setMessages(prev => {
              return prev.map(msg => msg.temporary && msg.content === message.content ? { ...message, msg_type: 'sent' } : msg)
            })
          }else {
            setMessages((prev) => [
              ...prev, { ...message, msg_type: 'received',  }
            ]);
          }
        }
      } 
      else if (data.type === "join_denied") {
        toast.error(data.payload.reason || "Failed to join the room.");
        navigate("/all-rooms");
      } 
      else if (data.type === "group_notification") {
        const messageRoomId = data.room_id;
        const subType = data.sub_type;
        const senderId = data.payload?.sender_id
        if (subType === 'joined' && senderId == userId) {
          fetchRoomDetails()
          fetchMessages()
          return
        } else if (subType === 'left' && senderId == userId) {
          return
        }
        if (messageRoomId === roomId) {
          toast.info(data.payload.message || '');
        }
      }
    });

    return () => {
      // exit room on unmount
      if (wsSend) {
        wsSend({ type: "left_room", room_id: roomId, payload: {} });
      }
    };
  }, [wsListen, roomId, setMessages, navigate, wsSend]);

  return null;
};

export default ChatEventHandler;