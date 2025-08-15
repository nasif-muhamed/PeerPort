import { Routes, Route } from "react-router-dom";

// guards
import ProtectedRoute from "./guards/ProtectedRoute";
import GuesRoute from "./guards/GuesRoute";

// pages
import Landing from "../pages/Landing";
import Register from "../pages/Register";
import Login from "../pages/Login";
import NotFound from "../pages/NotFound";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />

      {/* Guest Pages */}
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />

      {/* 404 Page */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default AppRoutes