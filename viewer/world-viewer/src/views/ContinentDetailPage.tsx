// src/pages/ContinentDetailPage.tsx
import React, { useEffect, useState, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Grid,
  Card,
  CardMedia,
  CardContent,
  CardActionArea,
} from "@mui/material";
import yaml from "js-yaml";
import EntityLayout from "../components/EntityLayout";

interface City {
  name: string;
  description?: string;
  image_path?: string;
}

interface Region {
  name: string;
  description?: string;
  image_path?: string;
}

interface Continent {
  name: string;
  description: string;
  image_path: string;
  cities: City[];
  regions: Region[];
}

export const ContinentDetailPage: React.FC = () => {
  const { worldId, continentId } = useParams();
  const [continent, setContinent] = useState<Continent | null>(null);
  const navigate = useNavigate();

  const decodedContinentId = useMemo(
    () => (continentId ? decodeURIComponent(continentId) : ""),
    [continentId]
  );

  useEffect(() => {
    if (!worldId || !decodedContinentId) return;
    fetch(`/worlds/${worldId}/world.yaml`)
      .then((res) => res.text())
      .then((text) => {
        const data = yaml.load(text) as any;
        const found = data?.continents?.find(
          (c: any) => (c.name || "").toLowerCase() === decodedContinentId.toLowerCase()
        );
        setContinent(found ?? null);
      })
      .catch((err) => {
        console.error("Failed to load continent:", err);
      });
  }, [worldId, decodedContinentId]);

  if (!continent || !worldId) return null;

  // Small helper to render a uniform card grid for cities/regions
  const renderSection = (
    title: string,
    items: Array<City | Region>,
    buildHref: (item: City | Region) => string
  ) => {
    if (!items?.length) return null;
    return (
      <>
        <Typography variant="h5" sx={{ mt: 6, mb: 2 }}>
          {title}
        </Typography>
        <Grid container spacing={3}>
          {items.map((item) => {
            const href = buildHref(item);
            const imgSrc = item.image_path
              ? `/worlds/${worldId}/${item.image_path.replace(/^\/+/, "")}`
              : undefined;

            return (
              <Grid key={item.name} size={{ xs: 12, sm: 6, md: 4 }}>
                <Card>
                  <CardActionArea onClick={() => navigate(href)}>
                    {imgSrc && (
                      <CardMedia
                        component="img"
                        height="160"
                        image={imgSrc}
                        alt={item.name}
                      />
                    )}
                    <CardContent>
                      <Typography variant="h6">{item.name}</Typography>
                      <Typography variant="body2" color="text.secondary" noWrap>
                        {item.description}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      </>
    );
  };

  return (
    <>
      <CssBaseline />
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6">World Explorer</Typography>
        </Toolbar>
      </AppBar>

      <EntityLayout
        worldId={worldId}
        title={continent.name}
        subtitle="Continent"
        imagePath={`/worlds/${worldId}/${continent.image_path?.replace(/^\/+/, "")}`}
        description={continent.description}
        // No children here since you render Cities/Regions grids below
        childrenItems={[]}
        breadcrumbLinks={[
          { label: "Worlds", href: "/" },
          { label: worldId!, href: `/worlds/${worldId}` },
          { label: continent.name }, // current page
        ]}
      />

      {/* Cities — full-width grid with onClick navigation */}
      {renderSection("Cities", continent.cities ?? [], (item) =>
        `/worlds/${worldId}/continents/${encodeURIComponent(continent.name)}/cities/${encodeURIComponent(item.name)}`
      )}

      {/* Regions — full-width grid with onClick navigation */}
      {renderSection("Regions", continent.regions ?? [], (item) =>
        `/worlds/${worldId}/continents/${encodeURIComponent(continent.name)}/regions/${encodeURIComponent(item.name)}`
      )}
    </>
  );
};

export default ContinentDetailPage;
