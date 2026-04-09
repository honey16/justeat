import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  getOwnerMenu,
  addMenuItem,
  updateMenuItem,
  deleteMenuItem,
  getOwnerRestaurant,
} from "@/services/endpoints";
import { Plus, Pencil, Trash2, Sparkles, Tag, ImageIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";

const specialLabels = [
  "",
  "Today's Special",
  "Deal of the Day",
  "Chef's Pick",
  "Limited Time",
];

export default function ManageMenu() {
  const queryClient = useQueryClient();
  const { data: restaurant } = useQuery({
    queryKey: ["ownerRestaurant"],
    queryFn: getOwnerRestaurant,
  });
  const { data: menu = [], isLoading } = useQuery({
    queryKey: ["ownerMenu"],
    queryFn: getOwnerMenu,
  });
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<any>(null);
  const [form, setForm] = useState({
    name: "",
    description: "",
    price: "",
    category: "",
    is_special: false,
    special_label: "",
    image: "",
  });

  const addMutation = useMutation({
    mutationFn: (data: any) =>
      addMenuItem({ ...data, restaurant_id: restaurant?.id }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ownerMenu"] });
      toast.success("Item added");
      setDialogOpen(false);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, ...data }: any) => updateMenuItem(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ownerMenu"] });
      toast.success("Item updated");
      setDialogOpen(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteMenuItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ownerMenu"] });
      toast.success("Item deleted");
    },
  });

  const openAdd = () => {
    setEditing(null);
    setForm({
      name: "",
      description: "",
      price: "",
      category: "",
      is_special: false,
      special_label: "",
      image: "",
    });
    setDialogOpen(true);
  };

  const openEdit = (item: any) => {
    setEditing(item);
    setForm({
      name: item.name,
      description: item.description,
      price: String(item.price),
      category: item.category,
      is_special: item.is_special || item.isSpecial,
      special_label: item.special_label || item.specialLabel || "",
      image: item.image || "",
    });
    setDialogOpen(true);
  };

  const handleSubmit = () => {
    const data = { ...form, price: parseFloat(form.price) };
    if (!data.name || !data.price || !data.category) {
      toast.error("Fill in all required fields");
      return;
    }
    if (editing) {
      updateMutation.mutate({ ...data, id: editing.id });
    } else {
      addMutation.mutate(data);
    }
  };

  const categories = [...new Set(menu.map((item: any) => item.category))];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">
            Manage Menu
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {menu.length} items
          </p>
        </div>
        <Button
          className="gradient-warm text-primary-foreground font-medium"
          onClick={openAdd}
        >
          <Plus className="mr-2 h-4 w-4" /> Add Item
        </Button>
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-20 rounded-xl" />
          ))}
        </div>
      ) : (
        categories.map((cat) => (
          <div key={cat as string} className="space-y-3">
            <h2 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
              {cat as string}
            </h2>
            {menu
              .filter((item: any) => item.category === cat)
              .map((item: any) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between rounded-xl border border-border bg-card p-4 transition-all hover:shadow-soft"
                >
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-medium text-foreground">
                        {item.name}
                      </h3>
                      {item.isSpecial && item.specialLabel && (
                        <Badge variant="secondary" className="gap-1 text-xs">
                          <Tag className="h-3 w-3" />
                          {item.specialLabel}
                        </Badge>
                      )}
                      {item.isSpecial && !item.specialLabel && (
                        <Sparkles className="h-3.5 w-3.5 text-primary" />
                      )}
                    </div>
                    <p className="mt-0.5 text-sm text-muted-foreground line-clamp-1">
                      {item.description}
                    </p>
                  </div>
                  <div className="flex items-center gap-3 ml-4">
                    <span className="text-sm font-semibold text-foreground">
                      ${item.price.toFixed(2)}
                    </span>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 text-muted-foreground hover:text-foreground"
                      onClick={() => openEdit(item)}
                    >
                      <Pencil className="h-3.5 w-3.5" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 text-muted-foreground hover:text-destructive"
                      onClick={() => deleteMutation.mutate(item.id)}
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
              ))}
          </div>
        ))
      )}

      {/* Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="bg-card border-border sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-foreground">
              {editing ? "Edit Item" : "Add Item"}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4 pt-2">
            <div className="space-y-2">
              <Label className="text-sm text-muted-foreground">Name</Label>
              <Input
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className="h-10 bg-secondary/50 border-border"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-sm text-muted-foreground">
                Description
              </Label>
              <Input
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
                className="h-10 bg-secondary/50 border-border"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-sm text-muted-foreground">
                  Price ($)
                </Label>
                <Input
                  type="number"
                  step="0.01"
                  value={form.price}
                  onChange={(e) => setForm({ ...form, price: e.target.value })}
                  className="h-10 bg-secondary/50 border-border"
                />
              </div>
              <div className="space-y-2">
                <Label className="text-sm text-muted-foreground">
                  Category
                </Label>
                <Input
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                  className="h-10 bg-secondary/50 border-border"
                />
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Switch
                checked={form.is_special}
                onCheckedChange={(v) =>
                  setForm({
                    ...form,
                    is_special: v,
                    special_label: v
                      ? form.special_label || "Today's Special"
                      : "",
                  })
                }
              />
              <Label className="text-sm text-foreground">Mark as special</Label>
            </div>
            {form.is_special && (
              <div className="space-y-2">
                <Label className="text-sm text-muted-foreground">
                  Special Label
                </Label>
                <Select
                  value={form.special_label}
                  onValueChange={(v) => setForm({ ...form, special_label: v })}
                >
                  <SelectTrigger className="h-10 bg-secondary/50 border-border">
                    <SelectValue placeholder="Select label" />
                  </SelectTrigger>
                  <SelectContent>
                    {specialLabels.filter(Boolean).map((label) => (
                      <SelectItem key={label} value={label}>
                        {label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
            <div className="space-y-2">
              <Label className="text-sm text-muted-foreground">Image URL</Label>
              <Input
                placeholder="https://example.com/item.jpg"
                value={form.image}
                onChange={(e) => setForm({ ...form, image: e.target.value })}
                className="h-10 bg-secondary/50 border-border"
              />
              {form.image && (
                <div className="mt-2 rounded-lg border border-border overflow-hidden h-24 w-24 bg-secondary/30">
                  <img
                    src={form.image}
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
                onClick={() => setDialogOpen(false)}
              >
                Cancel
              </Button>
              <Button
                className="flex-1 gradient-warm text-primary-foreground"
                onClick={handleSubmit}
              >
                {editing ? "Update" : "Add"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
