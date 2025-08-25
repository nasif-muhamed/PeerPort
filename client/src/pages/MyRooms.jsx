import { useState, useEffect, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";

import BackButton from "../components/BackButton";
import ChatButton from "../components/ChatButton";
import TypingIndicator from "../components/ui/TypingIndicator";
import { getMyRooms } from "../services/api/apiService";
import { handleError } from "../utils/handleError";

const MyRooms = () => {
  const [loading, setLoading] = useState(false);
  const [rooms, setRooms] = useState([]);
  const [nextUrl, setNextUrl] = useState(null);
  const observer = useRef();
  const navigate = useNavigate()

  const fetchMyRooms = async (url = null, append = false) => {
    setLoading(true);
    try {
      const { data } = await getMyRooms(url);
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
          fetchMyRooms(nextUrl, true);
        }
      });

      if (node) observer.current.observe(node);
    },
    [loading, nextUrl]
  );

  useEffect(() => {
    fetchMyRooms();
  }, []);

  const handleJoinRoom = (roomId) => {
    navigate(`/chat/${roomId}`)
  }

  const handleRoomSetting = (roomId) => {
    navigate(`/room-settings/${roomId}`)
  }

  return (
    <div className="min-h-screen px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <BackButton />

        <div className="space-y-4">
          {rooms.map((room, index) => (
            <div
              key={room.id}
              ref={index === rooms.length - 1 ? lastRoomElementRef : null}
              className="card-primary animate-chat-appear hover:border-accent-primary/50 cursor-pointer"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-semibold">{room.name}</h3>
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        room.status === "active"
                          ? "bg-accent-primary/20 text-accent-primary"
                          : "bg-text-muted/20 text-text-muted"
                      }`}
                    >
                      {room.status}
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-text-secondary">
                    <span>
                      {room.participant_count}/{room.limit} participants
                    </span>
                    <span>
                      Created {new Date(room.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>

                <div className="flex gap-2">
                  <ChatButton onClick={() => handleRoomSetting(room.id)} variant="secondary" className="text-sm px-4 py-2">
                    Settings
                  </ChatButton>

                  <ChatButton onClick={() => handleJoinRoom(room.id)} variant="primary" className="text-sm px-4 py-2">
                    Enter Room
                  </ChatButton>
                </div>
              </div>
            </div>
          ))}
        </div>

        {!loading && rooms.length === 0 && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">💬</div>
            <h3 className="text-xl font-semibold mb-2">No rooms yet</h3>
            <p className="text-text-secondary mb-6">
              Create your first chat room from the Dashboard
            </p>
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

export default MyRooms;
