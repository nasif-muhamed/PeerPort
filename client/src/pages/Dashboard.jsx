import { useState } from "react";
import { Link } from "react-router-dom";
import CreateRoomModal from "../components/CreateRoomModal";

const Dashboard = () => {
  const [showCreateModal, setShowCreateModal] = useState(false);
  return (
    <div className="min-h-screen px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Dashboard</h1>
          <p className="text-text-secondary text-lg">Choose how you want to start chatting</p>
        </div> */}

        {/* Chat-style Options */}
        <div className="max-w-2xl mx-auto space-y-6">
          {/* My Rooms */}
          <div className="flex justify-start animate-chat-appear">
            <div className="bg-chat-received text-text-primary rounded-2xl rounded-bl-md px-6 py-4 mr-auto max-w-md cursor-pointer hover:bg-chat-received-hover transition-colors">
              <Link to="/my-rooms" className="block">
                <div className="flex items-center gap-3">
                  <div className="text-2xl">🏠</div>
                  <div>
                    <h3 className="font-semibold text-lg">My Rooms</h3>
                    <p className="text-text-secondary text-sm">View and manage your created rooms</p>
                  </div>
                </div>
              </Link>
            </div>
          </div>

          {/* All Rooms */}
          <div className="flex justify-end animate-chat-appear">
            <div className="bg-chat-sent text-white rounded-2xl rounded-br-md px-6 py-4 ml-auto max-w-md cursor-pointer hover:bg-chat-sent-hover transition-colors">
              <Link to="/all-rooms" className="block">
                <div className="flex items-center gap-3">
                  <div className="text-2xl">🌐</div>
                  <div>
                    <h3 className="font-semibold text-lg">All Rooms</h3>
                    <p className="text-white/80 text-sm">Browse and join public rooms</p>
                  </div>
                </div>
              </Link>
            </div>
          </div>

          {/* Create Room */}
          <div onClick={() => setShowCreateModal(true)} className="flex justify-start animate-chat-appear">
            <div className="bg-chat-received text-text-primary rounded-2xl rounded-bl-md px-6 py-4 mr-auto max-w-md cursor-pointer hover:bg-chat-received-hover transition-colors">
              <div className="flex items-center gap-3">
                <div className="text-2xl">➕</div>
                <div>
                  <h3 className="font-semibold text-lg">Create New Room</h3>
                  <p className="text-text-secondary text-sm">Start a fresh conversation space</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-3 gap-6 mt-16">
          <div className="card-primary text-center animate-fade-in">
            <div className="text-3xl font-bold text-accent-primary mb-2">3</div>
            <p className="text-text-secondary">Active Rooms</p>
          </div>
          <div className="card-primary text-center animate-fade-in">
            <div className="text-3xl font-bold text-accent-secondary mb-2">12</div>
            <p className="text-text-secondary">Messages Today</p>
          </div>
          <div className="card-primary text-center animate-fade-in">
            <div className="text-3xl font-bold text-text-accent mb-2">5</div>
            <p className="text-text-secondary">Rooms Joined</p>
          </div>
        </div>
      </div>

      {showCreateModal && (
        <CreateRoomModal onClose={() => setShowCreateModal(false)} />
      )}
    </div>
  );
};

export default Dashboard;