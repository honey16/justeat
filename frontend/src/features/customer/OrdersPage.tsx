import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getCustomerOrders } from "@/services/endpoints";
import {
  Search,
  Package,
  Clock,
  CheckCircle2,
  ChefHat,
  Loader2,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

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

export default function OrdersPage() {
  const [search, setSearch] = useState("");
  const { data: orders = [], isLoading } = useQuery<any[]>({
    queryKey: ["customerOrders"],
    queryFn: () => getCustomerOrders(),
  });

  const filtered = (orders as any[]).filter(
    (o: any) =>
      o.restaurant_name?.toLowerCase().includes(search.toLowerCase()) ||
      o.items?.some((i: any) =>
        i.name?.toLowerCase().includes(search.toLowerCase()),
      ),
  );

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-semibold text-foreground">Your Orders</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Track and review your order history
        </p>
      </div>

      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Search orders..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-10 h-10 bg-card border-border"
        />
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-28 rounded-xl" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="rounded-xl border border-border bg-card p-12 text-center">
          <Package className="mx-auto h-8 w-8 text-muted-foreground/50" />
          <p className="mt-3 text-sm text-muted-foreground">No orders found</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((order: any) => {
            const status = statusConfig[order.status] || statusConfig.pending;
            const StatusIcon = status.icon;
            return (
              <div
                key={order.id}
                className="rounded-xl border border-border bg-card p-5 transition-all hover:shadow-soft"
              >
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <h3 className="font-medium text-foreground">
                      {order.restaurant_name}
                    </h3>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {order.items
                        ?.map((i: any) => `${i.name} × ${i.quantity}`)
                        .join(", ")}
                    </p>
                    <p className="mt-2 text-xs text-muted-foreground">
                      {new Date(order.created_at).toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                        year: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge className={`${status.className} border-0 gap-1`}>
                      <StatusIcon className="h-3 w-3" />
                      {status.label}
                    </Badge>
                    <span className="text-sm font-semibold text-foreground">
                      ${order.total?.toFixed(2)}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
