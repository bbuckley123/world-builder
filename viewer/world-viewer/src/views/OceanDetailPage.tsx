// src/pages/OceanDetailPage.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
} from "@mui/material";
import yaml from "js-yaml";
import EntityLayout from "../components/EntityLayout";

export const OceanDetailPage = () => {
  const { worldId, oceanId } = useParams();
  const [ocean, setOcean] = useState(null);

  useEffect(() => {
    if (!worldId || !oceanId) return;

    fetch(`/worlds/${worldId}/world.yaml`)
      .then((res) => res.text())
      .then((text) => {
        const data = yaml.load(text);
        const targetName = decodeURIComponent(oceanId);
        const found =
          data?.oceans?.find(
            (o) => (o.name || "").toLowerCase() === targetName.toLowerCase()
          ) || null;
        setOcean(found);
      })
      .catch((err) => {
        console.error("Failed to load ocean:", err);
      });
  }, [worldId, oceanId]);

  if (!ocean || !worldId) return null;

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
        imagePath={ocean.image_path ? `/worlds/${worldId}/${ocean.image_path}` : undefined}
        description={ocean.description}
        // Oceans currently have no children:
        childrenItems={[]}
        breadcrumbLinks={[
          { label: "Worlds", href: "/" },
          { label: worldId, href: `/world/${worldId}` },
          { label: ocean.name }, // current page (no href)
        ]}
      />
    </>
  );
};
