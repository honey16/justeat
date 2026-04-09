import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getRestaurantById,
  rateRestaurant,
  getCustomerPreferences,
  toggleFavoriteRestaurant,
} from "@/services/endpoints";
import { useCart } from "@/context/CartContext";
import {
  Star,
  Clock,
  ArrowLeft,
  Plus,
  Minus,
  Sparkles,
  Tag,
  ImageIcon,
  Heart,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";

function StarRating({
  rating,
  onRate,
}: {
  rating: number;
  onRate: (r: number) => void;
}) {
  const [hover, setHover] = useState(0);
  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          type="button"
          onClick={() => onRate(star)}
          onMouseEnter={() => setHover(star)}
          onMouseLeave={() => setHover(0)}
          className="transition-transform hover:scale-110"
        >
          <Star
            className={`h-5 w-5 transition-colors ${
              star <= (hover || rating)
                ? "fill-primary text-primary"
                : "text-muted-foreground/30"
            }`}
          />
        </button>
      ))}
      {rating > 0 && (
        <span className="ml-2 text-sm text-muted-foreground">{rating}/5</span>
      )}
    </div>
  );
}

export default function RestaurantDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { addItem, removeItem, items, updateQuantity } = useCart();
  const [userRating, setUserRating] = useState(0);

  const { data: restaurant, isLoading } = useQuery({
    queryKey: ["restaurant", id],
    queryFn: () => getRestaurantById(id!),
    enabled: !!id,
  });

  const { data: preferences } = useQuery({
    queryKey: ["customerPreferences"],
    queryFn: getCustomerPreferences,
  });

  const isFavorite =
    preferences?.favouriteRestaurants?.includes(id || "") || false;

  const rateMutation = useMutation({
    mutationFn: (rating: number) => rateRestaurant(id!, rating),
    onSuccess: (_, rating) => {
      setUserRating(rating);
      toast.success(`Rated ${rating} star${rating > 1 ? "s" : ""}`);
    },
  });

  const favoriteMutation = useMutation({
    mutationFn: () => toggleFavoriteRestaurant(id!, isFavorite),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customerPreferences"] });
      toast.success(
        isFavorite ? "Removed from favourites" : "Added to favourites",
      );
    },
  });

  const getItemQuantity = (itemId: string) => {
    const cartItem = items.find((i) => i.id === itemId);
    return cartItem?.quantity || 0;
  };

  const handleAdd = (item: any) => {
    addItem({
      id: item.id,
      name: item.name,
      price: item.price,
      restaurantId: restaurant!.id,
      restaurantName: restaurant!.name,
    });
  };

  const handleDecrease = (itemId: string) => {
    const cartItem = items.find((i) => i.id === itemId);
    if (cartItem) {
      if (cartItem.quantity <= 1) {
        removeItem(itemId);
      } else {
        updateQuantity(itemId, cartItem.quantity - 1);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6 animate-fade-in">
        <Skeleton className="h-48 w-full rounded-xl" />
        <Skeleton className="h-8 w-1/3" />
        <div className="grid gap-4 sm:grid-cols-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-28 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (!restaurant) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <p className="text-muted-foreground">Restaurant not found</p>
        <Button variant="ghost" className="mt-4" onClick={() => navigate(-1)}>
          <ArrowLeft className="mr-2 h-4 w-4" /> Go Back
        </Button>
      </div>
    );
  }

  const categories = [
    ...new Set(restaurant.menu.map((item: any) => item.category)),
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Back */}
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" /> Back to restaurants
      </button>

      {/* Hero */}
      <div
        className={`rounded-2xl bg-gradient-to-br ${restaurant.gradient} p-8 sm:p-10`}
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-white sm:text-3xl">
              {restaurant.name}
            </h1>
            <p className="mt-2 max-w-lg text-sm text-white/80">
              {restaurant.description}
            </p>
            {restaurant.email && (
              <p className="mt-2 text-sm text-white/80">{restaurant.email}</p>
            )}
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => favoriteMutation.mutate()}
            disabled={favoriteMutation.isPending}
            className="shrink-0 h-10 w-10 rounded-full bg-white/20 hover:bg-white/30 backdrop-blur-sm transition-all"
          >
            <Heart
              className={`h-5 w-5 transition-all ${
                isFavorite ? "fill-white text-white" : "text-white"
              }`}
            />
          </Button>
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <Badge className="bg-white/20 text-white border-0 backdrop-blur-sm">
            <Star className="mr-1 h-3 w-3 fill-white" /> {restaurant.rating}
          </Badge>
          <Badge className="bg-white/20 text-white border-0 backdrop-blur-sm">
            <Clock className="mr-1 h-3 w-3" /> {restaurant.deliveryTime}
          </Badge>
          <Badge className="bg-white/20 text-white border-0 backdrop-blur-sm">
            {restaurant.priceRange}
          </Badge>
          <Badge className="bg-white/20 text-white border-0 backdrop-blur-sm">
            {restaurant.cuisine}
          </Badge>
        </div>
      </div>

      {/* User Rating */}
      <div className="flex items-center gap-4 rounded-xl border border-border bg-card p-4">
        <span className="text-sm font-medium text-foreground">
          Rate this restaurant
        </span>
        <StarRating
          rating={userRating}
          onRate={(r) => rateMutation.mutate(r)}
        />
      </div>

      {/* Menu */}
      {categories.map((cat) => (
        <div key={cat as string} className="space-y-3">
          <h2 className="text-lg font-semibold text-foreground">
            {cat as string}
          </h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {restaurant.menu
              .filter((item: any) => item.category === cat)
              .map((item: any) => {
                const qty = getItemQuantity(item.id);
                return (
                  <div
                    key={item.id}
                    className="flex rounded-xl border border-border bg-card overflow-hidden transition-all hover:shadow-card"
                  >
                    {/* Image Placeholder */}
                    <div className="flex h-auto w-24 sm:w-28 shrink-0 items-center justify-center bg-muted">
                      <ImageIcon className="h-8 w-8 text-muted-foreground/30" />
                    </div>
                    {/* Content */}
                    <div className="flex flex-1 items-start justify-between p-4">
                      <div className="min-w-0 flex-1 pr-3">
                        <div className="flex items-center gap-2 flex-wrap">
                          <h3 className="font-medium text-foreground">
                            {item.name}
                          </h3>
                          {item.isSpecial && item.specialLabel && (
                            <Badge
                              variant="secondary"
                              className="gap-1 text-xs"
                            >
                              <Tag className="h-3 w-3" />
                              {item.specialLabel}
                            </Badge>
                          )}
                          {item.isSpecial && !item.specialLabel && (
                            <Sparkles className="h-3.5 w-3.5 text-primary shrink-0" />
                          )}
                        </div>
                        <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                          {item.description}
                        </p>
                        <p className="mt-2 text-sm font-semibold text-foreground">
                          ${item.price.toFixed(2)}
                        </p>
                      </div>
                      <div className="shrink-0">
                        {qty === 0 ? (
                          <Button
                            size="icon"
                            variant="outline"
                            className="h-9 w-9 rounded-lg border-border hover:gradient-warm hover:text-primary-foreground hover:border-transparent transition-all"
                            onClick={() => handleAdd(item)}
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                        ) : (
                          <div className="flex items-center gap-2">
                            <Button
                              size="icon"
                              variant="outline"
                              className="h-8 w-8 rounded-lg border-border"
                              onClick={() => handleDecrease(item.id)}
                            >
                              <Minus className="h-3.5 w-3.5" />
                            </Button>
                            <span className="w-6 text-center text-sm font-semibold text-foreground">
                              {qty}
                            </span>
                            <Button
                              size="icon"
                              variant="outline"
                              className="h-8 w-8 rounded-lg border-border"
                              onClick={() => handleAdd(item)}
                            >
                              <Plus className="h-3.5 w-3.5" />
                            </Button>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
          </div>
        </div>
      ))}
    </div>
  );
}
