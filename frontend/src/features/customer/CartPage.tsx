import { useNavigate } from "react-router-dom";
import { useCart } from "@/context/CartContext";
import {
  ShoppingCart,
  Minus,
  Plus,
  Trash2,
  ArrowRight,
  ArrowLeft,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import { placeOrder } from "@/services/endpoints";
import { useAuth } from "@/context/AuthContext";
import { useState } from "react";

export default function CartPage() {
  const { items, updateQuantity, removeItem, clearCart, total } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [placing, setPlacing] = useState(false);

  const handlePlaceOrder = async () => {
    if (items.length === 0) return;
    setPlacing(true);
    try {
      await placeOrder({
        restaurant_id: items[0].restaurantId,
        items: items.map((i) => ({ menu_item_id: i.id, quantity: i.quantity })),
      });
      clearCart();
      toast.success("Order placed successfully!");
      navigate("/customer/orders");
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to place order");
    } finally {
      setPlacing(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 animate-fade-in">
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-secondary">
          <ShoppingCart className="h-7 w-7 text-muted-foreground" />
        </div>
        <h2 className="mt-4 text-lg font-semibold text-foreground">
          Your cart is empty
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Discover restaurants and add items to get started.
        </p>
        <Button
          variant="outline"
          className="mt-6"
          onClick={() => navigate("/customer/dashboard")}
        >
          <ArrowLeft className="mr-2 h-4 w-4" /> Browse Restaurants
        </Button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <h1 className="text-2xl font-semibold text-foreground">Your Cart</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        From {items[0].restaurantName}
      </p>

      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        {/* Items */}
        <div className="lg:col-span-2 space-y-3">
          {items.map((item) => (
            <div
              key={item.id}
              className="flex items-center gap-4 rounded-xl border border-border bg-card p-4"
            >
              <div className="min-w-0 flex-1">
                <h3 className="font-medium text-foreground">{item.name}</h3>
                <p className="text-sm text-muted-foreground">
                  ${item.price.toFixed(2)} each
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="icon"
                  className="h-8 w-8 rounded-lg"
                  onClick={() => updateQuantity(item.id, item.quantity - 1)}
                >
                  <Minus className="h-3 w-3" />
                </Button>
                <span className="w-8 text-center text-sm font-medium text-foreground">
                  {item.quantity}
                </span>
                <Button
                  variant="outline"
                  size="icon"
                  className="h-8 w-8 rounded-lg"
                  onClick={() => updateQuantity(item.id, item.quantity + 1)}
                >
                  <Plus className="h-3 w-3" />
                </Button>
              </div>
              <p className="w-16 text-right text-sm font-semibold text-foreground">
                ${(item.price * item.quantity).toFixed(2)}
              </p>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-muted-foreground hover:text-destructive"
                onClick={() => removeItem(item.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>

        {/* Summary */}
        <div className="rounded-xl border border-border bg-card p-6 h-fit">
          <h3 className="font-semibold text-foreground">Order Summary</h3>
          <Separator className="my-4" />
          <div className="space-y-2 text-sm">
            <div className="flex justify-between text-muted-foreground">
              <span>Subtotal</span>
              <span>${total.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-muted-foreground">
              <span>Delivery</span>
              <span>Free</span>
            </div>
          </div>
          <Separator className="my-4" />
          <div className="flex justify-between font-semibold text-foreground">
            <span>Total</span>
            <span>${total.toFixed(2)}</span>
          </div>
          <Button
            className="mt-6 w-full h-11 gradient-warm text-primary-foreground font-medium"
            onClick={handlePlaceOrder}
            disabled={placing}
          >
            {placing ? (
              "Placing..."
            ) : (
              <>
                Place Order <ArrowRight className="ml-2 h-4 w-4" />
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
