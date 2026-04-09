import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "@/context/AuthContext";
import {
  getCustomerPreferences,
  saveCustomerPreferences,
  updateCustomerProfile,
  getCustomerProfile,
  getRestaurants,
} from "@/services/endpoints";
import {
  User,
  Mail,
  Phone,
  MapPin,
  Heart,
  Pencil,
  Save,
  X,
  ShieldCheck,
  Utensils,
  Star,
  Plus,
  Trash2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";

const allCuisines = [
  "Italian",
  "Japanese",
  "Indian",
  "French",
  "Mexican",
  "Korean",
  "American BBQ",
  "Mediterranean",
];
const allDietary = [
  "Vegetarian",
  "Vegan",
  "Gluten-Free",
  "Halal",
  "Kosher",
  "Dairy-Free",
  "Nut-Free",
];

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);

  const [profileForm, setProfileForm] = useState({
    name: user?.name || "",
    phone: user?.phone || "",
    address: user?.address || "",
  });

  const { data: preferences } = useQuery({
    queryKey: ["customerPreferences"],
    queryFn: getCustomerPreferences,
  });
  const { data: restaurants = [] } = useQuery<any[]>({
    queryKey: ["restaurants"],
    queryFn: () => getRestaurants(),
  });

  const [favCuisines, setFavCuisines] = useState<string[]>([]);
  const [favRestaurants, setFavRestaurants] = useState<string[]>([]);
  const [dietaryRestrictions, setDietaryRestrictions] = useState<string[]>([]);

  useEffect(() => {
    if (user) {
      setProfileForm({
        name: user.name || "",
        phone: user.phone || "",
        address: user.address || "",
      });
    }
  }, [user]);

  useEffect(() => {
    if (preferences) {
      setFavCuisines(preferences.favouriteCuisines || []);
      setFavRestaurants(preferences.favouriteRestaurants || []);
      setDietaryRestrictions(preferences.dietaryRestrictions || []);
    }
  }, [preferences]);

  const updateProfileMutation = useMutation({
    mutationFn: updateCustomerProfile,
    onSuccess: async () => {
      try {
        // Fetch the updated profile from backend
        const updatedProfile = await getCustomerProfile();
        // Update the user in AuthContext
        updateUser(updatedProfile);
        toast.success("Profile updated successfully");
      } catch (error) {
        console.error("Error updating user:", error);
        toast.error("Profile updated but failed to refresh data");
      }
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to update profile");
    },
  });

  const saveMutation = useMutation({
    mutationFn: () =>
      saveCustomerPreferences({
        favouriteCuisines: favCuisines,
        favouriteRestaurants: favRestaurants,
        dietaryRestrictions,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customerPreferences"] });
      toast.success("Preferences saved successfully");
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || "Failed to save preferences");
    },
  });

  const handleSave = async () => {
    try {
      // Save profile details
      await updateProfileMutation.mutateAsync(profileForm);

      // Save preferences
      await saveMutation.mutateAsync();

      setIsEditing(false);
    } catch (error) {
      console.error("Error saving:", error);
    }
  };

  const handleCancel = () => {
    if (preferences) {
      setFavCuisines(preferences.favouriteCuisines || []);
      setFavRestaurants(preferences.favouriteRestaurants || []);
      setDietaryRestrictions(preferences.dietaryRestrictions || []);
    }
    if (user) {
      setProfileForm({
        name: user.name || "",
        phone: user.phone || "",
        address: user.address || "",
      });
    }
    setIsEditing(false);
  };

  const addCuisine = (c: string) => {
    if (!favCuisines.includes(c)) setFavCuisines([...favCuisines, c]);
  };
  const removeCuisine = (c: string) =>
    setFavCuisines(favCuisines.filter((x) => x !== c));

  const addDietary = (d: string) => {
    if (!dietaryRestrictions.includes(d))
      setDietaryRestrictions([...dietaryRestrictions, d]);
  };
  const removeDietary = (d: string) =>
    setDietaryRestrictions(dietaryRestrictions.filter((x) => x !== d));

  const addFavRestaurant = (id: string) => {
    if (!favRestaurants.includes(id))
      setFavRestaurants([...favRestaurants, id]);
  };
  const removeFavRestaurant = (id: string) =>
    setFavRestaurants(favRestaurants.filter((x) => x !== id));

  const availableCuisines = allCuisines.filter((c) => !favCuisines.includes(c));
  const availableDietary = allDietary.filter(
    (d) => !dietaryRestrictions.includes(d),
  );
  const favRestaurantObjects = (restaurants as any[]).filter((r: any) =>
    favRestaurants.includes(r.id),
  );
  const availableRestaurants = (restaurants as any[]).filter(
    (r: any) => !favRestaurants.includes(r.id),
  );

  return (
    <div className="animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Profile</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your account settings
          </p>
        </div>
        {!isEditing ? (
          <Button
            variant="outline"
            className="gap-2"
            onClick={() => setIsEditing(true)}
          >
            <Pencil className="h-4 w-4" /> Edit
          </Button>
        ) : (
          <div className="flex gap-2">
            <Button variant="outline" className="gap-2" onClick={handleCancel}>
              <X className="h-4 w-4" /> Cancel
            </Button>
            <Button
              className="gradient-warm text-primary-foreground gap-2"
              onClick={handleSave}
              disabled={
                updateProfileMutation.isPending || saveMutation.isPending
              }
            >
              <Save className="h-4 w-4" />
              {updateProfileMutation.isPending || saveMutation.isPending
                ? "Saving..."
                : "Save"}
            </Button>
          </div>
        )}
      </div>

      <div className="mt-8 space-y-6">
        {/* Avatar */}
        <div className="flex items-center gap-4">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-secondary text-xl font-semibold text-secondary-foreground">
            {user?.name?.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="font-semibold text-foreground">{user?.name}</h2>
            <p className="text-sm text-muted-foreground capitalize">
              {user?.role} account
            </p>
          </div>
        </div>

        <Separator />

        {/* Details */}
        <div className="grid gap-5 sm:grid-cols-2">
          <div className="space-y-2">
            <Label className="text-sm text-muted-foreground">Full Name</Label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                value={profileForm.name}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, name: e.target.value })
                }
                className="pl-10 h-10 bg-card border-border"
                readOnly={!isEditing}
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label className="text-sm text-muted-foreground">Email</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                defaultValue={user?.email}
                className="pl-10 h-10 bg-card border-border"
                readOnly
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label className="text-sm text-muted-foreground">Phone</Label>
            <div className="relative">
              <Phone className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                value={profileForm.phone}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, phone: e.target.value })
                }
                className="pl-10 h-10 bg-card border-border"
                readOnly={!isEditing}
                placeholder="Enter phone number"
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label className="text-sm text-muted-foreground">Address</Label>
            <div className="relative">
              <MapPin className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                value={profileForm.address}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, address: e.target.value })
                }
                className="pl-10 h-10 bg-card border-border"
                readOnly={!isEditing}
                placeholder="Enter address"
              />
            </div>
          </div>
        </div>

        <Separator />

        {/* Favourite Cuisines */}
        <div>
          <h3 className="flex items-center gap-2 font-medium text-foreground">
            <Utensils className="h-4 w-4 text-primary" /> Favourite Cuisines
          </h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {favCuisines.length === 0 && (
              <p className="text-sm text-muted-foreground">
                No favourite cuisines selected
              </p>
            )}
            {favCuisines.map((c) => (
              <Badge
                key={c}
                variant="secondary"
                className="gap-1.5 px-3 py-1.5 text-sm"
              >
                {c}
                {isEditing && (
                  <button
                    onClick={() => removeCuisine(c)}
                    className="ml-0.5 hover:text-destructive transition-colors"
                  >
                    <X className="h-3 w-3" />
                  </button>
                )}
              </Badge>
            ))}
          </div>
          {isEditing && availableCuisines.length > 0 && (
            <div className="mt-3">
              <Select onValueChange={addCuisine}>
                <SelectTrigger className="w-[200px] h-9 bg-card border-border text-sm">
                  <Plus className="h-3.5 w-3.5 mr-1.5 text-muted-foreground" />
                  <SelectValue placeholder="Add cuisine..." />
                </SelectTrigger>
                <SelectContent>
                  {availableCuisines.map((c) => (
                    <SelectItem key={c} value={c}>
                      {c}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>

        {/* Dietary Restrictions */}
        <div>
          <h3 className="flex items-center gap-2 font-medium text-foreground">
            <ShieldCheck className="h-4 w-4 text-primary" /> Dietary
            Restrictions
          </h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {dietaryRestrictions.length === 0 && (
              <p className="text-sm text-muted-foreground">
                No dietary restrictions set
              </p>
            )}
            {dietaryRestrictions.map((d) => (
              <Badge
                key={d}
                variant="secondary"
                className="gap-1.5 px-3 py-1.5 text-sm"
              >
                {d}
                {isEditing && (
                  <button
                    onClick={() => removeDietary(d)}
                    className="ml-0.5 hover:text-destructive transition-colors"
                  >
                    <X className="h-3 w-3" />
                  </button>
                )}
              </Badge>
            ))}
          </div>
          {isEditing && availableDietary.length > 0 && (
            <div className="mt-3">
              <Select onValueChange={addDietary}>
                <SelectTrigger className="w-[200px] h-9 bg-card border-border text-sm">
                  <Plus className="h-3.5 w-3.5 mr-1.5 text-muted-foreground" />
                  <SelectValue placeholder="Add restriction..." />
                </SelectTrigger>
                <SelectContent>
                  {availableDietary.map((d) => (
                    <SelectItem key={d} value={d}>
                      {d}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>

        {/* Favourite Restaurants */}
        <div>
          <h3 className="flex items-center gap-2 font-medium text-foreground">
            <Heart className="h-4 w-4 text-primary" /> Favourite Restaurants
          </h3>
          <div className="mt-3 grid gap-2 sm:grid-cols-2">
            {favRestaurantObjects.length === 0 && (
              <p className="text-sm text-muted-foreground">
                No favourite restaurants yet
              </p>
            )}
            {favRestaurantObjects.map((r: any) => (
              <div
                key={r.id}
                className="flex items-center gap-3 rounded-xl border border-primary/20 bg-primary/5 p-3"
              >
                <div
                  className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br ${r.gradient}`}
                >
                  <Star className="h-4 w-4 text-white" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium text-foreground">
                    {r.name}
                  </p>
                  <p className="text-xs text-muted-foreground">{r.cuisine}</p>
                </div>
                {isEditing && (
                  <button
                    onClick={() => removeFavRestaurant(r.id)}
                    className="text-muted-foreground hover:text-destructive transition-colors"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                )}
              </div>
            ))}
          </div>
          {isEditing && availableRestaurants.length > 0 && (
            <div className="mt-3">
              <Select onValueChange={addFavRestaurant}>
                <SelectTrigger className="w-[240px] h-9 bg-card border-border text-sm">
                  <Plus className="h-3.5 w-3.5 mr-1.5 text-muted-foreground" />
                  <SelectValue placeholder="Add restaurant..." />
                </SelectTrigger>
                <SelectContent>
                  {availableRestaurants.map((r: any) => (
                    <SelectItem key={r.id} value={r.id}>
                      {r.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
