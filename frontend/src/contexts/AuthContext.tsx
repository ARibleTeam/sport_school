import React, { createContext, useState, useContext } from 'react';

interface AuthContextProps {
  isAdmin: boolean;
  setAdmin: (isAdmin: boolean) => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAdmin, setIsAdmin] = useState(false);

  const setAdmin = (isAdmin: boolean) => {
    setIsAdmin(isAdmin);
  };

  return (
    <AuthContext.Provider value={{ isAdmin, setAdmin }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
