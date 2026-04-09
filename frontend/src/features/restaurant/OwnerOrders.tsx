import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getOwnerOrders, updateOrderStatus } from "@/services/endpoints";
import { Clock, ChefHat, CheckCircle2, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";

const statusFlow: Record<string, string> = {
  pending: "preparing",
  preparing: "delivered",
};

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

export default function OwnerOrders() {
  const queryClient = useQueryClient();
  const { data: orders = [], isLoading } = useQuery<any[]>({
    queryKey: ["ownerOrders"],
    queryFn: () => getOwnerOrders(),
  });

  const mutation = useMutation({
    mutationFn: ({ id, status }: { id: string; status: string }) =>
      updateOrderStatus(id, status),
    onMutate: async ({ id, status }) => {
      await queryClient.cancelQueries({ queryKey: ["ownerOrders"] });
      const prev = queryClient.getQueryData(["ownerOrders"]);
      queryClient.setQueryData(["ownerOrders"], (old: any[]) =>
        old.map((o) => (o.id === id ? { ...o, status } : o)),
      );
      return { prev };
    },
    onError: (_err, _vars, ctx) => {
      queryClient.setQueryData(["ownerOrders"], ctx?.prev);
      toast.error("Failed to update status");
    },
    onSuccess: () => toast.success("Order status updated"),
  });

  const [filter, setFilter] = useState("all");
  const filtered =
    filter === "all"
      ? orders
      : (orders as any[]).filter((o: any) => o.status === filter);

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-semibold text-foreground">Orders</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Manage incoming orders
        </p>
      </div>

      {/* Filter */}
      <div className="flex flex-wrap gap-2">
        {["all", "pending", "preparing", "delivered"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`rounded-full px-3.5 py-1.5 text-sm font-medium capitalize transition-colors ${
              filter === f
                ? "gradient-warm text-primary-foreground"
                : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
            }`}
          >
            {f === "all" ? "All" : f}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-24 rounded-xl" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="rounded-xl border border-border bg-card p-12 text-center">
          <p className="text-sm text-muted-foreground">
            No orders in this category
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((order: any) => {
            const status = statusConfig[order.status] || statusConfig.pending;
            const StatusIcon = status.icon;
            const nextStatus = statusFlow[order.status];
            return (
              <div
                key={order.id}
                className="rounded-xl border border-border bg-card p-5 transition-all hover:shadow-soft"
              >
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium text-foreground">
                        {order.customerName}
                      </h3>
                      <Badge
                        className={`${status.className} border-0 gap-1 text-xs`}
                      >
                        <StatusIcon className="h-3 w-3" />
                        {status.label}
                      </Badge>
                    </div>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {order.items
                        .map((i: any) => `${i.name} × ${i.quantity}`)
                        .join(", ")}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {new Date(order.createdAt).toLocaleTimeString("en-US", {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-semibold text-foreground">
                      ${order.total.toFixed(2)}
                    </span>
                    {nextStatus && (
                      <Button
                        size="sm"
                        className="gradient-warm text-primary-foreground text-xs font-medium"
                        onClick={() =>
                          mutation.mutate({ id: order.id, status: nextStatus })
                        }
                        disabled={mutation.isPending}
                      >
                        {nextStatus === "preparing"
                          ? "Start Preparing"
                          : "Mark Delivered"}
                        <ArrowRight className="ml-1 h-3 w-3" />
                      </Button>
                    )}
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
