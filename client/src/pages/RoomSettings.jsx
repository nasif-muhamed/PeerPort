import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import BackButton from "../components/BackButton";
import ChatButton from "../components/ChatButton";
import ChatInput from "../components/ChatInput";

const RoomSettings = () => {
  const { roomId } = useParams();
  const navigate = useNavigate();
  
  const [room, setRoom] = useState({
    id: roomId,
    name: "General Chat",
    maxLimit: 15,
    isActive: true,
    isPrivate: false,
    participants: [
      { id: 1, name: "You", status: "online", isOwner: true },
      { id: 2, name: "Alice", status: "online", isOwner: false },
      { id: 3, name: "Bob", status: "away", isOwner: false },
      { id: 4, name: "Charlie", status: "online", isOwner: false }
    ]
  });

  const [pendingRequests] = useState([
    { id: 1, name: "Diana", requestedAt: "2 hours ago" },
    { id: 2, name: "Eve", requestedAt: "1 hour ago" }
  ]);

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleToggleStatus = () => {
    setRoom(prev => ({ ...prev, isActive: !prev.isActive }));
  };

  const handleTogglePrivacy = () => {
    setRoom(prev => ({ ...prev, isPrivate: !prev.isPrivate }));
  };

  const handleRemoveParticipant = (participantId) => {
    setRoom(prev => ({
      ...prev,
      participants: prev.participants.filter(p => p.id !== participantId)
    }));
  };

  const handleAcceptRequest = (requestId) => {
    console.log(`Accept request ${requestId}`);
    // Mock: move from pending to participants
  };

  const handleRejectRequest = (requestId) => {
    console.log(`Reject request ${requestId}`);
  };

  const handleDeleteRoom = () => {
    console.log("Room deleted");
    navigate("/my-rooms");
  };

  const handleUpdateLimit = (newLimit) => {
    setRoom(prev => ({ ...prev, maxLimit: parseInt(newLimit) || 1 }));
  };

  return (
    <div className="min-h-screen px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <BackButton to={`/chat/${roomId}`} />
        
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Room Settings</h1>
          <p className="text-text-secondary">Manage "{room.name}" room</p>
        </div>

        <div className="space-y-6">
          {/* Room Status */}
          <div className="card-primary">
            <h3 className="text-xl font-semibold mb-4">Room Status</h3>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Room is {room.isActive ? 'Active' : 'Inactive'}</p>
                <p className="text-text-secondary text-sm">
                  {room.isActive ? 'Users can join and chat' : 'Room is temporarily disabled'}
                </p>
              </div>
              <ChatButton
                variant={room.isActive ? "secondary" : "primary"}
                onClick={handleToggleStatus}
              >
                {room.isActive ? 'Deactivate' : 'Activate'}
              </ChatButton>
            </div>
          </div>

          {/* Privacy Settings */}
          <div className="card-primary">
            <h3 className="text-xl font-semibold mb-4">Privacy Settings</h3>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{room.isPrivate ? 'Private Room' : 'Public Room'}</p>
                <p className="text-text-secondary text-sm">
                  {room.isPrivate ? 'Users need approval to join' : 'Anyone can join directly'}
                </p>
              </div>
              <ChatButton
                variant="secondary"
                onClick={handleTogglePrivacy}
              >
                Make {room.isPrivate ? 'Public' : 'Private'}
              </ChatButton>
            </div>
          </div>

          {/* Participant Limit */}
          <div className="card-primary">
            <h3 className="text-xl font-semibold mb-4">Participant Limit</h3>
            <div className="flex items-center gap-4">
              <div className="flex-1 max-w-xs">
                <ChatInput
                  type="number"
                  value={room.maxLimit}
                  onChange={(e) => handleUpdateLimit(e.target.value)}
                  variant="received"
                  min="1"
                />
              </div>
              <span className="text-text-secondary">participants maximum</span>
            </div>
          </div>

          {/* Current Participants */}
          <div className="card-primary">
            <h3 className="text-xl font-semibold mb-4">
              Current Participants ({room.participants.length})
            </h3>
            <div className="space-y-3">
              {room.participants.map((participant) => (
                <div key={participant.id} className="flex items-center justify-between p-3 bg-background-secondary rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${
                      participant.status === 'online' ? 'bg-accent-primary' : 'bg-text-muted'
                    }`} />
                    <span>{participant.name}</span>
                    {participant.isOwner && (
                      <span className="text-xs bg-accent-primary/20 text-accent-primary px-2 py-1 rounded">
                        Owner
                      </span>
                    )}
                  </div>
                  {!participant.isOwner && (
                    <ChatButton
                      variant="secondary"
                      className="text-sm px-3 py-1"
                      onClick={() => handleRemoveParticipant(participant.id)}
                    >
                      Remove
                    </ChatButton>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Pending Requests (only for private rooms) */}
          {room.isPrivate && pendingRequests.length > 0 && (
            <div className="card-primary">
              <h3 className="text-xl font-semibold mb-4">
                Pending Requests ({pendingRequests.length})
              </h3>
              <div className="space-y-3">
                {pendingRequests.map((request) => (
                  <div key={request.id} className="flex items-center justify-between p-3 bg-background-secondary rounded-lg">
                    <div>
                      <p className="font-medium">{request.name}</p>
                      <p className="text-text-secondary text-sm">Requested {request.requestedAt}</p>
                    </div>
                    <div className="flex gap-2">
                      <ChatButton
                        variant="primary"
                        className="text-sm px-3 py-1"
                        onClick={() => handleAcceptRequest(request.id)}
                      >
                        Accept
                      </ChatButton>
                      <ChatButton
                        variant="secondary"
                        className="text-sm px-3 py-1"
                        onClick={() => handleRejectRequest(request.id)}
                      >
                        Reject
                      </ChatButton>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Danger Zone */}
          <div className="card-primary border-red-500/20">
            <h3 className="text-xl font-semibold mb-4 text-red-400">Danger Zone</h3>
            {!showDeleteConfirm ? (
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-red-400">Delete Room</p>
                  <p className="text-text-secondary text-sm">
                    This action cannot be undone. All messages will be lost.
                  </p>
                </div>
                <ChatButton
                  variant="secondary"
                  onClick={() => setShowDeleteConfirm(true)}
                  className="border-red-500/50 text-red-400 hover:bg-red-500/10"
                >
                  Delete Room
                </ChatButton>
              </div>
            ) : (
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
                <p className="text-red-400 font-medium mb-4">
                  Are you sure you want to delete this room?
                </p>
                <div className="flex gap-3">
                  <ChatButton
                    variant="primary"
                    onClick={handleDeleteRoom}
                    className="bg-red-500 hover:bg-red-600 text-white"
                  >
                    Yes, Delete Room
                  </ChatButton>
                  <ChatButton
                    variant="secondary"
                    onClick={() => setShowDeleteConfirm(false)}
                  >
                    Cancel
                  </ChatButton>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RoomSettings;