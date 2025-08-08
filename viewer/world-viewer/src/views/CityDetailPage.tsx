// src/pages/CityDetailPage.tsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import yaml from "js-yaml";
import { AppBar, Toolbar, Typography, CssBaseline } from "@mui/material";
import EntityLayout from "../components/EntityLayout";

type City = {
  name: string;
  description?: string;
  image_path?: string;
};

type Continent = {
  name: string;
  cities?: City[];
};

export const CityDetailPage: React.FC = () => {
  const { worldId, continentId, cityId } = useParams();
  const [city, setCity] = useState<City | null>(null);

  useEffect(() => {
    if (!worldId || !continentId || !cityId) return;
    fetch(`/worlds/${worldId}/world.yaml`)
      .then((res) => res.text())
      .then((text) => {
        const data = yaml.load(text) as any;
        const targetContinentName = decodeURIComponent(continentId);
        const targetCityName = decodeURIComponent(cityId);

        const continent: Continent | undefined = data?.continents?.find(
            (c: any) => (c.name || "").toLowerCase() === targetContinentName.toLowerCase()
        );

        const found =
          continent?.cities?.find(
            (ct) => (ct.name || "").toLowerCase() === targetCityName.toLowerCase()
          ) ?? null;

        setCity(found);
      })
      .catch((err) => console.error("Failed to load city:", err));
  }, [worldId, continentId, cityId]);

  if (!city || !worldId) return null;

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
        title={city.name}
        subtitle="City"
        imagePath={city.image_path ? `/worlds/${worldId}/${city.image_path}` : undefined}
        description={city.description}
        // no children for cities (for now)
        childrenItems={[]}
        breadcrumbLinks={[
          { label: "Worlds", href: "/" },
          { label: worldId!, href: `/world/${worldId}` },
          { label: decodeURIComponent(continentId!), href: `/world/${worldId}/continent/${continentId}` },
          { label: city.name },
        ]}
      />
    </>
  );
};

export default CityDetailPage;
