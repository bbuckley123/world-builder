// src/pages/RegionDetailPage.tsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import yaml from "js-yaml";
import { AppBar, Toolbar, Typography, CssBaseline } from "@mui/material";
import EntityLayout from "../components/EntityLayout";

type Region = {
  name: string;
  description?: string;
  image_path?: string;
};

type Continent = {
  name: string;
  regions?: Region[];
};

export const RegionDetailPage: React.FC = () => {
  const { worldId, continentId, regionId } = useParams();
  const [region, setRegion] = useState<Region | null>(null);

  useEffect(() => {
    if (!worldId || !continentId || !regionId) return;
    fetch(`/worlds/${worldId}/world.yaml`)
      .then((res) => res.text())
      .then((text) => {
        const data = yaml.load(text) as any;
        const targetContinentName = decodeURIComponent(continentId);
        const targetRegionName = decodeURIComponent(regionId);

        const continent: Continent | undefined = data?.continents?.find(
          (c: any) => (c.name || "").toLowerCase() === targetContinentName.toLowerCase()
        );

        const found =
          continent?.regions?.find(
            (r) => (r.name || "").toLowerCase() === targetRegionName.toLowerCase()
          ) ?? null;

        setRegion(found);
      })
      .catch((err) => console.error("Failed to load region:", err));
  }, [worldId, continentId, regionId]);

  if (!region || !worldId) return null;

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
        title={region.name}
        subtitle="Region"
        imagePath={region.image_path ? `/worlds/${worldId}/${region.image_path}` : undefined}
        description={region.description}
        // no children for regions (for now)
        childrenItems={[]}
        breadcrumbLinks={[
          { label: "Worlds", href: "/" },
          { label: worldId!, href: `/worlds/${worldId}` },
          { label: decodeURIComponent(continentId!), href: `/worlds/${worldId}/continents/${continentId}` },
          { label: region.name },
        ]}
      />
    </>
  );
};

export default RegionDetailPage;
