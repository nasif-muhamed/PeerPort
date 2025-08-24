import { useState, useEffect, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";

import BackButton from "../components/BackButton";
import ChatButton from "../components/ChatButton";
import ChatInput from "../components/ChatInput";
import TypingIndicator from "../components/ui/TypingIndicator";
import { getAllRooms } from "../services/api/api_service";
import { handleError } from "../utils/handleError";
import { useDebounce } from "../hooks/useDebounce"

const AllRooms = () => {
  const [loading, setLoading] = useState(false);
  const [rooms, setRooms] = useState([]);
  const [nextUrl, setNextUrl] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const observer = useRef();
  const navigate = useNavigate()
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  const fetchAllRooms = async (url = null, append = false) => {
    setLoading(true);
    try {
      const { data } = await getAllRooms(url, searchTerm);
      setRooms(prev => (append ? [...prev, ...data.results] : data.results));
      setNextUrl(data.next);
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };

  const lastRoomElementRef = useCallback(
    node => {
      if (loading) return;
      if (observer.current) observer.current.disconnect();

      observer.current = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && nextUrl) {
          fetchAllRooms(nextUrl, true);
        }
      });

      if (node) observer.current.observe(node);
    },
    [loading, nextUrl]
  );

  useEffect(() => {
    fetchAllRooms();
  }, [debouncedSearchTerm]);

  const handleJoinRoom = (roomId) => {
    navigate(`/chat/${roomId}`)
  }

  return (
    <div className="min-h-screen px-4 py-8">
      <div className="max-w-4xl mx-auto">

        {/* Search */}
        <div className="mb-8 flex items-center gap-5">
          <BackButton className="!mb-0" />

          <div className="max-w-md">
            <ChatInput
              name={'search'}
              placeholder="Search rooms..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              variant="received"
              className="w-full"
            />
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {rooms.map((room, index) => (
            <div 
              key={room.id} 
              className="card-primary animate-chat-appear hover:border-accent-primary/50"
              ref={index === rooms.length - 1 ? lastRoomElementRef : null}
            >
              <div className="flex items-start justify-between gap-4 mb-4">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-1">{room.name}</h3>
                  <p className="text-text-secondary text-sm">by {room.owner?.username}</p>
                </div>
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-accent-primary/20 text-accent-primary">
                  {room.access}
                </span>
              </div>
              
              <div className="flex items-center justify-between gap-4">
                <div className="text-sm text-text-secondary">
                  <span>{room.participants}/{room.limit} participants</span>
                </div>
                
                <ChatButton 
                  variant="primary" 
                  className="text-sm px-4 py-2"
                  disabled={room.participant_count >= room.limit}
                  onClick={room.participant_count < room.limit ? () => handleJoinRoom(room.id) : null}
                >
                  {room.participant_count >= room.limit ? 'Room Full' : 'Join Room'}
                </ChatButton>
              </div>
            </div>
          ))}
        </div>

        {!loading && rooms.length === 0 && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🌐</div>
            <h3 className="text-xl font-semibold mb-2">No public rooms available</h3>
            <p className="text-text-secondary">Be the first to create a public room!</p>
          </div>
        )}

        {loading && (
          <div className="flex justify-center items-center w-full py-6">
            <TypingIndicator />
          </div>
        )}

      </div>
    </div>
  );
};

export default AllRooms;