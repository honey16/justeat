import apiClient from "./api";
import { mockLocations } from "@/mock/data";

// Auth
export const loginUser = async (email: string, password: string) => {
  const response = await apiClient.post("/auth/login", { email, password });
  return {
    user: response.data.user,
    token: response.data.access_token,
  };
};

export const registerUser = async (userData: {
  email: string;
  password: string;
  name: string;
  role: "customer" | "owner";
  phone?: string;
  address?: string;
  restaurant_id?: string;
}) => {
  const response = await apiClient.post("/auth/register", userData);
  return {
    user: response.data.user,
    token: response.data.access_token,
  };
};

export const resetPassword = async (
  email: string,
  oldPassword: string,
  newPassword: string,
) => {
  const response = await apiClient.post("/auth/reset-password", {
    email,
    old_password: oldPassword,
    new_password: newPassword,
  });
  return response.data;
};

// Restaurants
export const getRestaurants = async (filters?: {
  location?: string;
  cuisine?: string;
  query?: string;
  price_range?: string;
}) => {
  const response = await apiClient.get("/restaurants", { params: filters });
  return response.data;
};

export const getRestaurantById = async (id: string) => {
  const response = await apiClient.get(`/restaurants/${id}`);
  return response.data;
};

export const getRestaurantMenu = async (id: string, category?: string) => {
  const response = await apiClient.get(`/restaurants/${id}/menu`, {
    params: category ? { category } : {},
  });
  return response.data;
};

export const getRestaurantSpecials = async (id: string) => {
  const response = await apiClient.get(`/restaurants/${id}/specials`);
  return response.data;
};

export const getRestaurantPopular = async (id: string) => {
  const response = await apiClient.get(`/restaurants/${id}/popular`);
  return response.data;
};

// Locations
export const getLocations = async () => {
  return mockLocations; // Keep mock for now as it's just a static list
};

// Customer Orders
export const getCustomerOrders = async (filters?: {
  status?: string;
  query?: string;
}) => {
  const response = await apiClient.get("/customer/orders", { params: filters });
  return response.data;
};

export const getCustomerOrderById = async (orderId: string) => {
  const response = await apiClient.get(`/customer/orders/${orderId}`);
  return response.data;
};

export const placeOrder = async (orderData: {
  restaurant_id: string;
  items: Array<{ menu_item_id: string; quantity: number }>;
}) => {
  const response = await apiClient.post("/customer/orders", orderData);
  return response.data;
};

// Customer Profile
export const getCustomerProfile = async () => {
  const response = await apiClient.get("/customer/profile");
  return response.data;
};

export const updateCustomerProfile = async (profileData: {
  name?: string;
  phone?: string;
  address?: string;
}) => {
  const response = await apiClient.put("/customer/profile", profileData);
  return response.data;
};

// Owner
export const getOwnerOrders = async (filters?: { status?: string }) => {
  const response = await apiClient.get("/owner/orders", { params: filters });
  return response.data;
};

export const getOwnerOrderById = async (orderId: string) => {
  const response = await apiClient.get(`/owner/orders/${orderId}`);
  return response.data;
};

export const updateOrderStatus = async (orderId: string, status: string) => {
  const response = await apiClient.put(`/owner/orders/${orderId}/status`, {
    status,
  });
  return response.data;
};

export const getOwnerMenu = async () => {
  const response = await apiClient.get("/owner/menu");
  return response.data;
};

export const getOwnerRestaurant = async () => {
  const response = await apiClient.get("/owner/restaurant");
  return response.data;
};

export const createRestaurant = async (restaurantData: any) => {
  const response = await apiClient.post("/owner/restaurant", restaurantData);
  return response.data;
};

export const updateRestaurantDetails = async (restaurantData: any) => {
  const response = await apiClient.put("/owner/restaurant", restaurantData);
  return response.data;
};

export const addMenuItem = async (itemData: any) => {
  const response = await apiClient.post("/owner/menu", itemData);
  return response.data;
};

export const updateMenuItem = async (itemId: string, itemData: any) => {
  const response = await apiClient.put(`/owner/menu/${itemId}`, itemData);
  return response.data;
};

export const deleteMenuItem = async (itemId: string) => {
  const response = await apiClient.delete(`/owner/menu/${itemId}`);
  return response.data;
};

export const getPopularItems = async (limit?: number) => {
  const response = await apiClient.get("/owner/analytics/popular-items", {
    params: limit ? { limit } : {},
  });
  return response.data;
};

// Recommendations
export const getRecommendations = async () => {
  const response = await apiClient.get("/customer/recommendations");
  return response.data.restaurants;
};

// Ratings (placeholder - can be extended when backend supports it)
export const rateRestaurant = async (restaurantId: string, rating: number) => {
  // TODO: Implement backend endpoint for ratings
  console.log(`Rating restaurant ${restaurantId} with ${rating} stars`);
  return { restaurantId, rating };
};

// Customer Preferences
export const getCustomerPreferences = async () => {
  const response = await apiClient.get("/customer/preferences");
  return {
    favouriteRestaurants: response.data.favorite_restaurants,
    favouriteCuisines: response.data.favorite_cuisines,
    dietaryRestrictions: response.data.dietary_restrictions,
  };
};

export const saveCustomerPreferences = async (prefs: {
  favouriteRestaurants: string[];
  favouriteCuisines: string[];
  dietaryRestrictions: string[];
}) => {
  const response = await apiClient.put("/customer/preferences", {
    favorite_restaurants: prefs.favouriteRestaurants,
    favorite_cuisines: prefs.favouriteCuisines,
    dietary_restrictions: prefs.dietaryRestrictions,
  });
  return {
    favouriteRestaurants: response.data.favorite_restaurants,
    favouriteCuisines: response.data.favorite_cuisines,
    dietaryRestrictions: response.data.dietary_restrictions,
  };
};

export const toggleFavoriteRestaurant = async (
  restaurantId: string,
  isFavorite: boolean,
) => {
  const prefs = await getCustomerPreferences();
  const currentFavorites = prefs.favouriteRestaurants || [];
  const updatedFavorites = isFavorite
    ? currentFavorites.filter((id: string) => id !== restaurantId)
    : [...currentFavorites, restaurantId];

  return saveCustomerPreferences({
    favouriteRestaurants: updatedFavorites,
    favouriteCuisines: prefs.favouriteCuisines || [],
    dietaryRestrictions: prefs.dietaryRestrictions || [],
  });
};
