import ChatNavbar from './ChatNavbar';

const AuthenticatedLayout = ({ 
  children, 
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
        {children}
      </div>
    </div>
  );
};

export default AuthenticatedLayout;
