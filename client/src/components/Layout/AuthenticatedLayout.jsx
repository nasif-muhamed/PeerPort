import ChatNavbar from './ChatNavbar';
import { Outlet } from 'react-router-dom';

const AuthenticatedLayout = ({ 
  username = "User",
}) => {
  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <ChatNavbar 
        username={username} 
      />
      
      {/* Page Content with proper spacing to avoid navbar overlap */}
      <div className="pt-24 sm:pt-20">
        <Outlet />
      </div>
    </div>
  );
};

export default AuthenticatedLayout;
