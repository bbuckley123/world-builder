// src/pages/OceanDetailPage.tsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { CssBaseline, AppBar, Toolbar, Typography } from "@mui/material";
import yaml from "js-yaml";
import EntityLayout from "../components/EntityLayout";

interface Ocean {
  name: string;
  description?: string;
  image_path?: string;
}

export const OceanDetailPage: React.FC = () => {
  const { worldId, oceanId } = useParams<{ worldId: string; oceanId: string }>();
  const [ocean, setOcean] = useState<Ocean | null>(null);

  useEffect(() => {
    if (!worldId || !oceanId) return;

    fetch(`/worlds/${worldId}/world.yaml`)
      .then((res) => res.text())
      .then((text) => {
        const data = yaml.load(text) as { oceans?: Ocean[] } | undefined;
        const target = decodeURIComponent(oceanId);
        const found =
          data?.oceans?.find(
            (o) => (o.name || "").toLowerCase() === target.toLowerCase()
          ) ?? null;

        setOcean(found);
      })
      .catch((err) => {
        console.error("Failed to load ocean:", err);
      });
  }, [worldId, oceanId]);

  if (!ocean || !worldId) return null;

  const imgPath = ocean.image_path
    ? `/worlds/${worldId}/${ocean.image_path.replace(/^\/+/, "")}`
    : undefined;

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
        title={ocean.name}
        subtitle="Ocean"
        imagePath={imgPath}
        description={ocean.description}
        childrenItems={[]}
        breadcrumbLinks={[
          { label: "Worlds", href: "/" },
          { label: worldId, href: `/worlds/${worldId}` }, 
          { label: ocean.name }, // current page
        ]}
      />
    </>
  );
};

export default OceanDetailPage;
