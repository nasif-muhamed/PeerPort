import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import BackButton from "../components/BackButton";
import ChatButton from "../components/ChatButton";
import ChatInput from "../components/ChatInput";
import ChatLoader from "../components/ui/ChatLoader";
import { handleError } from "../utils/handleError";
import { getMyRoom, updateMyRoom, deleteMyRoom } from "../services/api/apiService";
import { useDebounce } from "../hooks/useDebounce";
import { toast } from "sonner";
import { useAuthTokens } from "../hooks/useAuthTokens"


const RoomSettings = () => {
  const { roomId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [room, setRoom] = useState({});
  const [isEditing, setIsEditing] = useState(false);
  const [newName, setNewName] = useState("");
  const [pendingRequests, setPendingRequests] = useState([]);
  const [limitInput, setLimitInput] = useState("");
  const debouncedLimit = useDebounce(limitInput, 500);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const { userId } = useAuthTokens()

  const fetchMyRoom = async () => {
    setLoading(true);
    try {
      const { data } = await getMyRoom(roomId);
      setRoom(data);
      setNewName(data.name);
      setLimitInput(data.limit?.toString() ?? "0");
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMyRoom();
  }, []);

  const updateRoom = async (body) => {
    setLoading(true);
    try {
      const { data } = await updateMyRoom(roomId, body);
      setRoom(data);
      setNewName(data.name);
      setLimitInput(data.limit?.toString() ?? "0");
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleUpdateName = () => {
    if (isEditing && newName !== room.name) {
      updateRoom({ name: newName });
    }
    setIsEditing(!isEditing);
  };

  const handleToggleStatus = () => {
    updateRoom({ status: room.status === "active" ? "inactive" : "active" });
  };

  const handleTogglePrivacy = () => {
    updateRoom({ access: room.access === "private" ? "public" : "private" });
  };

  useEffect(() => {
    if (debouncedLimit && debouncedLimit !== room.limit?.toString()) {
      updateRoom({ limit: parseInt(debouncedLimit, 10) });
    }
  }, [debouncedLimit]);

  // const handleRemoveParticipant = (participantId) => {
  //   setRoom((prev) => ({
  //     ...prev,
  //     participants: prev.participants.filter((p) => p.id !== participantId),
  //   }));
  // };

  // const handleAcceptRequest = (requestId) => {
  //   console.log(`Accept request ${requestId}`);
  // };

  // const handleRejectRequest = (requestId) => {
  //   console.log(`Reject request ${requestId}`);
  // };

  const handleDeleteRoom = async () => {
    setLoading(true);
    try {
      const { status } = await deleteMyRoom(roomId);
      if (status === 200 || status === 204) {
        toast.info(`Successfully deleted room: ${room.name}`)
        navigate("/my-rooms", { replace: true });
      } else {
        throw new Error("Unexpected response while deleting room");
      }
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen px-4 py-8">
      {loading && (
        <div className="flex justify-center items-center w-full py-6">
          <ChatLoader />
        </div>
      )}
      {Object.entries(room).length > 0 && (
        <div className="max-w-4xl mx-auto">
          <BackButton to={`/my-rooms`} />

          <div className="space-y-6">
            {/* Room Name */}
            <div className="card-primary">
              <div className="flex items-center justify-between">
                <input
                  className={`px-4 py-2 text-xl font-semibold bg-transparent focus:outline-none ${
                    isEditing ? "border-black border-2 rounded-md" : "border-none"
                  }`}
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  disabled={!isEditing}
                />
                <ChatButton
                  variant={isEditing ? "secondary" : "primary"}
                  onClick={handleToggleUpdateName}
                >
                  {isEditing ? "Update" : "Edit"}
                </ChatButton>
              </div>
            </div>

            {/* Room Status */}
            <div className="card-primary">
              <h3 className="text-xl font-semibold mb-4">Room Status</h3>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">
                    Room is {room.status === "active" ? "Active" : "Inactive"}
                  </p>
                  <p className="text-text-secondary text-sm">
                    {room.status === "active"
                      ? "Users can join and chat"
                      : "Room is temporarily disabled"}
                  </p>
                </div>
                <ChatButton
                  variant={room.status === "active" ? "secondary" : "primary"}
                  onClick={handleToggleStatus}
                >
                  {room.status === "active" ? "Deactivate" : "Activate"}
                </ChatButton>
              </div>
            </div>

            {/* Privacy Settings */}
            <div className="card-primary">
              <h3 className="text-xl font-semibold mb-4">Privacy Settings</h3>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">
                    {room.access === "private" ? "Private Room" : "Public Room"}
                  </p>
                  <p className="text-text-secondary text-sm">
                    {room.access === "private"
                      ? "Users need approval to join"
                      : "Anyone can join directly"}
                  </p>
                </div>
                <ChatButton
                  variant="secondary"
                  onClick={handleTogglePrivacy}
                >
                  Make {room.access === "private" ? "Public" : "Private"}
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
                    value={limitInput}
                    onChange={(e) => setLimitInput(e.target.value)}
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
                Current Participants ({room.participants?.length ?? 0})
              </h3>
              <div className="space-y-3">
                {room.participants?.map((participant) => (
                  <div
                    key={participant.id}
                    className="flex items-center justify-between p-3 bg-background-secondary rounded-lg"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-3 h-3 rounded-full ${
                          participant.status === "online"
                            ? "bg-accent-primary"
                            : "bg-text-muted"
                        }`}
                      />
                      <span>{participant.username}</span>
                      {participant.id == userId && (
                        <span className="text-xs bg-accent-primary/20 text-accent-primary px-2 py-1 rounded">
                          Owner
                        </span>
                      )}
                    </div>
                    {/* {!(participant.id == userId) && (
                      <ChatButton
                        variant="secondary"
                        className="text-sm px-3 py-1"
                        onClick={() => handleRemoveParticipant(participant.id)}
                      >
                        Remove
                      </ChatButton>
                    )} */}
                  </div>
                ))}
              </div>
            </div>

            {/* Pending Requests (only for private rooms) */}
            {room.access === "private" && pendingRequests.length > 0 && (
              <div className="card-primary">
                <h3 className="text-xl font-semibold mb-4">
                  Pending Requests ({pendingRequests.length})
                </h3>
                <div className="space-y-3">
                  {pendingRequests.map((request) => (
                    <div
                      key={request.id}
                      className="flex items-center justify-between p-3 bg-background-secondary rounded-lg"
                    >
                      <div>
                        <p className="font-medium">{request.name}</p>
                        <p className="text-text-secondary text-sm">
                          Requested {request.requestedAt}
                        </p>
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
              <h3 className="text-xl font-semibold mb-4 text-red-400">
                Danger Zone
              </h3>
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
      )}
    </div>
  );
};

export default RoomSettings;