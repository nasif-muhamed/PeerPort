import { Routes, Route } from "react-router-dom";

// guards & layout
import ProtectedRoute from "./guards/ProtectedRoute";
import GuestRoute from "./guards/GuestRoute";
import AuthenticatedLayout from "../components/Layout/AuthenticatedLayout";

// pages
import Landing from "../pages/Landing";
import Register from "../pages/Register";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import MyRooms from "../pages/MyRooms";
import AllRooms from "../pages/AllRooms";
import ChatPage from "../pages/ChatPage";
import NotFound from "../pages/NotFound";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />

      {/* Guest Pages */}
      <Route element={<GuestRoute/>}>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Route>

      <Route element={<ProtectedRoute/>}>
        <Route element={<AuthenticatedLayout/>}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/my-rooms" element={<MyRooms />} />
          <Route path="/all-rooms" element={<AllRooms />} />
        </Route>
        <Route path="/chat/:roomId" element={<ChatPage />} />
      </Route>

      {/* 404 Page */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default AppRoutes