import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getOwnerOrders,
  getOwnerMenu,
  getOwnerRestaurant,
  updateRestaurantDetails,
} from "@/services/endpoints";
import { useAuth } from "@/context/AuthContext";
import {
  TrendingUp,
  ShoppingCart,
  Star,
  DollarSign,
  ChefHat,
  Clock,
  CheckCircle2,
  Pencil,
  Save,
  X,
  ImageIcon,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { toast } from "sonner";

const statusConfig: Record<
  string,
  { label: string; icon: any; className: string }
> = {
  pending: {
    label: "Pending",
    icon: Clock,
    className: "bg-secondary text-secondary-foreground",
  },
  preparing: {
    label: "Preparing",
    icon: ChefHat,
    className: "bg-primary/10 text-primary",
  },
  delivered: {
    label: "Delivered",
    icon: CheckCircle2,
    className:
      "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
  },
};

export default function OwnerDashboard() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const { data: orders = [], isLoading: ordersLoading } = useQuery<any[]>({
    queryKey: ["ownerOrders"],
    queryFn: () => getOwnerOrders(),
  });
  const { data: menu = [] } = useQuery<any[]>({
    queryKey: ["ownerMenu"],
    queryFn: () => getOwnerMenu(),
  });
  const { data: restaurant } = useQuery({
    queryKey: ["ownerRestaurant"],
    queryFn: () => getOwnerRestaurant(),
  });

  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editForm, setEditForm] = useState({
    name: "",
    email: "",
    cuisine: "",
    priceRange: "",
    deliveryTime: "",
    description: "",
    image: "",
  });

  const updateMutation = useMutation({
    mutationFn: updateRestaurantDetails,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ownerRestaurant"] });
      toast.success("Restaurant details updated");
      setEditDialogOpen(false);
    },
  });

  const openEditDialog = () => {
    if (restaurant) {
      setEditForm({
        name: restaurant.name,
        email: restaurant.email || "",
        cuisine: restaurant.cuisine,
        priceRange: restaurant.priceRange,
        deliveryTime: restaurant.deliveryTime,
        description: restaurant.description,
        image: restaurant.image || "",
      });
    }
    setEditDialogOpen(true);
  };

  const totalRevenue = (orders as any[]).reduce(
    (sum: number, o: any) => sum + o.total,
    0,
  );
  const avgRating = 4.8;

  const stats = [
    {
      label: "Total Orders",
      value: orders.length,
      icon: ShoppingCart,
      color: "text-primary",
    },
    {
      label: "Revenue",
      value: `$${totalRevenue.toFixed(0)}`,
      icon: DollarSign,
      color: "text-green-600 dark:text-green-400",
    },
    {
      label: "Avg Rating",
      value: avgRating,
      icon: Star,
      color: "text-amber-500",
    },
    {
      label: "Menu Items",
      value: menu.length,
      icon: ChefHat,
      color: "text-muted-foreground",
    },
  ];

  const itemCounts: Record<string, number> = {};
  (orders as any[]).forEach((o: any) =>
    o.items.forEach((i: any) => {
      itemCounts[i.name] = (itemCounts[i.name] || 0) + i.quantity;
    }),
  );
  const topItems = Object.entries(itemCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Dashboard</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Welcome back, {user?.name}
            {restaurant ? ` — ${restaurant.name}` : ""}
          </p>
        </div>
        <Button variant="outline" className="gap-2" onClick={openEditDialog}>
          <Pencil className="h-4 w-4" /> Edit Restaurant
        </Button>
      </div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((s) => (
          <div
            key={s.label}
            className="rounded-xl border border-border bg-card p-5"
          >
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">{s.label}</span>
              <s.icon className={`h-4 w-4 ${s.color}`} />
            </div>
            <p className="mt-2 text-2xl font-semibold text-foreground">
              {s.value}
            </p>
          </div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Top Items */}
        <div className="rounded-xl border border-border bg-card p-6">
          <h2 className="flex items-center gap-2 font-semibold text-foreground">
            <TrendingUp className="h-4 w-4 text-primary" /> Most Ordered Items
          </h2>
          <div className="mt-4 space-y-3">
            {topItems.length === 0 ? (
              <p className="text-sm text-muted-foreground">No data yet</p>
            ) : (
              topItems.map(([name, count], i) => (
                <div key={name} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-secondary text-xs font-medium text-secondary-foreground">
                      {i + 1}
                    </span>
                    <span className="text-sm text-foreground">{name}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">
                    {count} orders
                  </span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent Orders */}
        <div className="rounded-xl border border-border bg-card p-6">
          <h2 className="font-semibold text-foreground">Recent Orders</h2>
          {ordersLoading ? (
            <div className="mt-4 space-y-3">
              {Array.from({ length: 3 }).map((_, i) => (
                <Skeleton key={i} className="h-14 rounded-lg" />
              ))}
            </div>
          ) : (
            <div className="mt-4 space-y-3">
              {(orders as any[]).slice(0, 5).map((order: any) => {
                const status =
                  statusConfig[order.status] || statusConfig.pending;
                const StatusIcon = status.icon;
                return (
                  <div
                    key={order.id}
                    className="flex items-center justify-between rounded-lg bg-secondary/50 p-3"
                  >
                    <div>
                      <p className="text-sm font-medium text-foreground">
                        {order.customerName}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {order.items.map((i: any) => i.name).join(", ")}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge
                        className={`${status.className} border-0 gap-1 text-xs`}
                      >
                        <StatusIcon className="h-3 w-3" />
                        {status.label}
                      </Badge>
                      <span className="text-sm font-medium text-foreground">
                        ${order.total.toFixed(2)}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Edit Restaurant Dialog */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent className="bg-card border-border sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-foreground">
              Edit Restaurant Details
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4 pt-2">
            <div className="space-y-2">
              <Label className="text-sm text-muted-foreground">
                Restaurant Name
              </Label>
              <Input
                value={editForm.name}
                onChange={(e) =>
                  setEditForm({ ...editForm, name: e.target.value })
                }
                className="h-10 bg-secondary/50 border-border"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-sm text-muted-foreground">Email</Label>
              <Input
                type="email"
                placeholder="contact@restaurant.com"
                value={editForm.email}
                onChange={(e) =>
                  setEditForm({ ...editForm, email: e.target.value })
                }
                className="h-10 bg-secondary/50 border-border"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-sm text-muted-foreground">Cuisine</Label>
                <Input
                  value={editForm.cuisine}
                  onChange={(e) =>
                    setEditForm({ ...editForm, cuisine: e.target.value })
                  }
                  className="h-10 bg-secondary/50 border-border"
                />
              </div>
              <div className="space-y-2">
                <Label className="text-sm text-muted-foreground">
                  Price Range
                </Label>
                <Input
                  value={editForm.priceRange}
                  onChange={(e) =>
                    setEditForm({ ...editForm, priceRange: e.target.value })
                  }
                  className="h-10 bg-secondary/50 border-border"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label className="text-sm text-muted-foreground">
                Delivery Time
              </Label>
              <Input
                value={editForm.deliveryTime}
                onChange={(e) =>
                  setEditForm({ ...editForm, deliveryTime: e.target.value })
                }
                className="h-10 bg-secondary/50 border-border"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-sm text-muted-foreground">
                Description
              </Label>
              <Input
                value={editForm.description}
                onChange={(e) =>
                  setEditForm({ ...editForm, description: e.target.value })
                }
                className="h-10 bg-secondary/50 border-border"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-sm text-muted-foreground">Image URL</Label>
              <Input
                placeholder="https://example.com/image.jpg"
                value={editForm.image}
                onChange={(e) =>
                  setEditForm({ ...editForm, image: e.target.value })
                }
                className="h-10 bg-secondary/50 border-border"
              />
              {editForm.image && (
                <div className="mt-2 rounded-lg border border-border overflow-hidden h-32 bg-secondary/30">
                  <img
                    src={editForm.image}
                    alt="Preview"
                    className="h-full w-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).style.display = "none";
                    }}
                  />
                </div>
              )}
            </div>
            <div className="flex gap-3 pt-2">
              <Button
                variant="outline"
                className="flex-1"
                onClick={() => setEditDialogOpen(false)}
              >
                Cancel
              </Button>
              <Button
                className="flex-1 gradient-warm text-primary-foreground"
                onClick={() => updateMutation.mutate(editForm)}
              >
                Save Changes
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
