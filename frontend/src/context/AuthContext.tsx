/* Auth Context */
import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
  useMemo,
  useCallback,
} from "react";
import { loginUser } from "@/services/endpoints";

interface User {
  id: string;
  email: string;
  role: string;
  name: string;
  restaurant_id?: string;
  phone?: string;
  address?: string;
  created_at?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  updateUser: (updatedUser: Partial<User>) => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem("auth_user");
    const token = localStorage.getItem("auth_token");
    if (stored && token) {
      try {
        setUser(JSON.parse(stored));
      } catch {
        // Clear invalid data
        localStorage.removeItem("auth_user");
        localStorage.removeItem("auth_token");
      }
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    try {
      const { user: u, token } = await loginUser(email, password);
      setUser(u as User);
      localStorage.setItem("auth_user", JSON.stringify(u));
      localStorage.setItem("auth_token", token);
    } catch (error: any) {
      console.error("Login error:", error);
      console.error("Error response:", error.response?.data);
      throw error;
    }
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem("auth_user");
    localStorage.removeItem("auth_token");
  }, []);

  const updateUser = useCallback((updatedUser: Partial<User>) => {
    setUser((prevUser) => {
      if (!prevUser) return prevUser;
      const newUser = { ...prevUser, ...updatedUser };
      localStorage.setItem("auth_user", JSON.stringify(newUser));
      return newUser;
    });
  }, []);

  const value = useMemo(
    () => ({
      user,
      isLoading,
      login,
      logout,
      updateUser,
      isAuthenticated: !!user,
    }),
    [user, isLoading, login, logout, updateUser],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
