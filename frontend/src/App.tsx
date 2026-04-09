import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider } from "@/context/ThemeContext";
import { CartProvider } from "@/context/CartContext";
import ProtectedRoute from "@/features/auth/ProtectedRoute";
import AppLayout from "@/components/layout/AppLayout";
import LoginPage from "@/features/auth/LoginPage";
import CustomerDashboard from "@/features/customer/Dashboard";
import RestaurantDetails from "@/features/customer/RestaurantDetails";
import CartPage from "@/features/customer/CartPage";
import OrdersPage from "@/features/customer/OrdersPage";
import ProfilePage from "@/features/customer/ProfilePage";
import OwnerDashboard from "@/features/restaurant/OwnerDashboard";
import ManageMenu from "@/features/restaurant/ManageMenu";
import OwnerOrders from "@/features/restaurant/OwnerOrders";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 1000 * 60 * 5, retry: 1 },
  },
});

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider>
      <AuthProvider>
        <CartProvider>
          <TooltipProvider>
            <Sonner />
            <BrowserRouter>
              <Routes>
                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route path="/login" element={<LoginPage />} />

                {/* Customer Routes */}
                <Route element={<ProtectedRoute role="customer"><AppLayout /></ProtectedRoute>}>
                  <Route path="/customer/dashboard" element={<CustomerDashboard />} />
                  <Route path="/customer/restaurant/:id" element={<RestaurantDetails />} />
                  <Route path="/customer/cart" element={<CartPage />} />
                  <Route path="/customer/orders" element={<OrdersPage />} />
                  <Route path="/customer/profile" element={<ProfilePage />} />
                </Route>

                {/* Owner Routes */}
                <Route element={<ProtectedRoute role="owner"><AppLayout /></ProtectedRoute>}>
                  <Route path="/owner/dashboard" element={<OwnerDashboard />} />
                  <Route path="/owner/menu" element={<ManageMenu />} />
                  <Route path="/owner/orders" element={<OwnerOrders />} />
                </Route>

                <Route path="*" element={<NotFound />} />
              </Routes>
            </BrowserRouter>
          </TooltipProvider>
        </CartProvider>
      </AuthProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;
