import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import BackButton from "../components/BackButton";
import ChatLoader from "../components/ui/ChatLoader";
import MessageInput from "../components/chat-page/MessageInput";
import { getRoomDetials, getMessages } from "../services/api/apiService";
import { handleError } from "../utils/handleError"
import ChatEventHandler from "../components/chat-page/ChatEventHandler";
import MessageArea from "../components/chat-page/MessageArea";
import { ChatNotificationSocketProvider } from '../context/ChatNotificationSocketContext'; 

const ChatPage = () => {
  const { roomId } = useParams();
  const navigate = useNavigate()  
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState([]);
  const [room, setRoom] = useState({});
  const [chatLoading, setChatLoading] = useState(false)
  
  // Pagination state
  const [loadingOlderMessages, setLoadingOlderMessages] = useState(false);
  const [nextPageUrl, setNextPageUrl] = useState(null);
  const [hasMoreMessages, setHasMoreMessages] = useState(true);

  const fetchRoomDetails = async () => {
    setLoading(true)
    try {
      const { data } = await getRoomDetials(roomId);
      setRoom(data)
    } catch (error) {
      handleError(error)
      navigate(-1)
    } finally {
      setLoading(false)
    }
  }

  const fetchMessages = async () => {
    try {
      const { data } = await getMessages(roomId);
      setMessages(data?.results || [])
      setNextPageUrl(data?.next || null)
      setHasMoreMessages(!!data?.next)
    } catch (error) {
      handleError(error)
    } finally {
      setChatLoading(false)
    }
  }

  // Function to load older messages
  const loadOlderMessages = async () => {
    if (!nextPageUrl || loadingOlderMessages) return;

    setLoadingOlderMessages(true);
    try {
      // Extract the page parameter from the next URL
      const url = new URL(nextPageUrl);
      const page = url.searchParams.get('page');
      
      // Call your API service with the page parameter
      const { data } = await getMessages(roomId, page);
      
      // Prepend older messages to the current messages array
      setMessages(prevMessages => [...(data?.results || []), ...prevMessages]);
      
      // Update pagination state
      setNextPageUrl(data?.next || null);
      setHasMoreMessages(!!data?.next);
      
    } catch (error) {
      handleError(error);
    } finally {
      setLoadingOlderMessages(false);
    }
  };
  
  return (
    <ChatNotificationSocketProvider endpoint={`/ws/room/${roomId}/`}>
      <div className="flex h-screen overflow-hidden">
        <ChatEventHandler 
          fetchRoomDetails={fetchRoomDetails}
          fetchMessages={fetchMessages}
          setMessages={setMessages}
          room={room}
          setRoom={setRoom}
        />

        {loading && <ChatLoader/>}

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <div className="border-b border-border-primary rounded-none p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <BackButton className="!mb-0"/>
                <div>
                  <h1 className="text-xl font-semibold">{room.name}</h1>
                  <p className="text-text-secondary text-sm">
                    {room.participant_count} participants
                  </p>
                </div>
              </div>
              {/* <button className="text-red-500 hover:text-red-400 font-medium px-3 py-1 hover:bg-red-500/10 rounded transition-colors">
                Leave Room
              </button> */}
            </div>
          </div>
          {/* Messages Area */}
          <MessageArea 
            messages={messages} 
            chatLoading={chatLoading}
            loadingOlderMessages={loadingOlderMessages}
            onLoadMore={loadOlderMessages}
            hasMoreMessages={hasMoreMessages}
          />
          {/* Message Input */}
          <MessageInput roomId={roomId} setMessages={setMessages} />
        </div>
      </div>
    </ChatNotificationSocketProvider>
  );
};

export default ChatPage;