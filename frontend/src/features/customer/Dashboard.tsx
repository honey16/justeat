import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import {
  getRestaurants,
  getRecommendations,
  getLocations,
} from "@/services/endpoints";
import { useAuth } from "@/context/AuthContext";
import {
  Search,
  Star,
  Clock,
  Sparkles,
  ChevronRight,
  MapPin,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const cuisineOptions = [
  "All",
  "Italian",
  "Japanese",
  "Indian",
  "French",
  "Mexican",
  "Korean",
  "American BBQ",
  "Mediterranean",
];
const priceOptions = ["All", "$", "$$", "$$$"];
const sortOptions = [
  "Default",
  "Rating: High to Low",
  "Rating: Low to High",
  "Delivery Time",
  "Name A–Z",
];

export default function CustomerDashboard() {
  const { user } = useAuth();
  const [search, setSearch] = useState("");
  const [cuisine, setCuisine] = useState("All");
  const [price, setPrice] = useState("All");
  const [location, setLocation] = useState("All Locations");
  const [sortBy, setSortBy] = useState("Default");

  const { data: restaurants = [], isLoading } = useQuery<any[]>({
    queryKey: ["restaurants"],
    queryFn: () => getRestaurants(),
  });
  const { data: recommendations = [] } = useQuery<any[]>({
    queryKey: ["recommendations"],
    queryFn: getRecommendations,
  });
  const { data: locations = [] } = useQuery<string[]>({
    queryKey: ["locations"],
    queryFn: getLocations,
  });

  const filtered = restaurants
    .filter((r: any) => {
      if (
        search &&
        !r.name.toLowerCase().includes(search.toLowerCase()) &&
        !r.cuisine.toLowerCase().includes(search.toLowerCase())
      )
        return false;
      if (cuisine !== "All" && r.cuisine !== cuisine) return false;
      if (price !== "All" && r.priceRange !== price) return false;
      if (location !== "All Locations" && r.location !== location) return false;
      return true;
    })
    .sort((a: any, b: any) => {
      switch (sortBy) {
        case "Rating: High to Low":
          return b.rating - a.rating;
        case "Rating: Low to High":
          return a.rating - b.rating;
        case "Delivery Time":
          return parseInt(a.deliveryTime) - parseInt(b.deliveryTime);
        case "Name A–Z":
          return a.name.localeCompare(b.name);
        default:
          return 0;
      }
    });

  const hasActiveFilters =
    search ||
    cuisine !== "All" ||
    price !== "All" ||
    location !== "All Locations";

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold text-foreground sm:text-3xl">
          Good evening, {user?.name?.split(" ")[0]}
        </h1>
        <p className="mt-1 text-muted-foreground">
          What are you in the mood for?
        </p>
      </div>

      {/* Search + Filters Row */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:flex-wrap">
        <div className="relative flex-1 min-w-[200px] max-w-sm">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search restaurants or cuisines..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10 h-10 bg-card border-border"
          />
        </div>

        <Select value={location} onValueChange={setLocation}>
          <SelectTrigger className="w-[160px] h-10 bg-card border-border">
            <MapPin className="h-3.5 w-3.5 mr-1.5 text-muted-foreground shrink-0" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {locations.map((loc: string) => (
              <SelectItem key={loc} value={loc}>
                {loc}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={cuisine} onValueChange={setCuisine}>
          <SelectTrigger className="w-[160px] h-10 bg-card border-border">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {cuisineOptions.map((c) => (
              <SelectItem key={c} value={c}>
                {c === "All" ? "All Cuisines" : c}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={price} onValueChange={setPrice}>
          <SelectTrigger className="w-[140px] h-10 bg-card border-border">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {priceOptions.map((p) => (
              <SelectItem key={p} value={p}>
                {p === "All" ? "Any Price" : p}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-[180px] h-10 bg-card border-border">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {sortOptions.map((s) => (
              <SelectItem key={s} value={s}>
                {s}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Recommendations */}
      {recommendations.length > 0 && !hasActiveFilters && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">
              Recommended for You
            </h2>
          </div>
          <div className="grid gap-4 sm:grid-cols-3">
            {recommendations.map((r: any) => (
              <Link
                key={r.id}
                to={`/customer/restaurant/${r.id}`}
                className="group flex items-center gap-3 rounded-xl border border-border bg-card p-3 transition-all hover:shadow-card"
              >
                <div
                  className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br ${r.gradient}`}
                >
                  <Star className="h-5 w-5 text-white" />
                </div>
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-foreground">
                    {r.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {r.cuisine} · {r.rating}
                  </p>
                </div>
                <ChevronRight className="ml-auto h-4 w-4 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Restaurant Grid */}
      <div>
        <h2 className="mb-4 text-lg font-semibold text-foreground">
          {hasActiveFilters ? `${filtered.length} results` : "All Restaurants"}
        </h2>
        {isLoading ? (
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div
                key={i}
                className="rounded-xl border border-border bg-card overflow-hidden"
              >
                <Skeleton className="h-40 w-full" />
                <div className="p-4 space-y-2">
                  <Skeleton className="h-5 w-2/3" />
                  <Skeleton className="h-4 w-1/2" />
                </div>
              </div>
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="rounded-xl border border-border bg-card p-12 text-center">
            <Search className="mx-auto h-8 w-8 text-muted-foreground/50" />
            <p className="mt-3 text-sm text-muted-foreground">
              No restaurants found. Try adjusting your filters.
            </p>
          </div>
        ) : (
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((r: any) => (
              <Link
                key={r.id}
                to={`/customer/restaurant/${r.id}`}
                className="group overflow-hidden rounded-xl border border-border bg-card transition-all hover:shadow-card"
              >
                <div
                  className={`flex h-40 items-center justify-center bg-gradient-to-br ${r.gradient}`}
                >
                  <span className="text-3xl font-bold text-white/20 uppercase tracking-widest">
                    {r.cuisine}
                  </span>
                </div>
                <div className="p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
                        {r.name}
                      </h3>
                      <p className="mt-0.5 text-sm text-muted-foreground">
                        {r.cuisine} · {r.priceRange}
                      </p>
                    </div>
                    <Badge
                      variant="secondary"
                      className="flex items-center gap-1 shrink-0"
                    >
                      <Star className="h-3 w-3 fill-primary text-primary" />
                      {r.rating}
                    </Badge>
                  </div>
                  <div className="mt-3 flex items-center gap-3 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Clock className="h-3.5 w-3.5" />
                      {r.deliveryTime}
                    </span>
                    <span className="flex items-center gap-1">
                      <MapPin className="h-3.5 w-3.5" />
                      {r.location}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
