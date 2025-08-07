import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Breadcrumbs,
  Link,
} from "@mui/material";
import EntityLayout from "../components/EntityLayout"; // adjust path if needed
import yaml from "js-yaml";

interface City {
  name: string;
  description?: string;
  image_path?: string;
}

interface Continent {
  name: string;
  description: string;
  image_path: string;
  cities: City[];
}

export const ContinentDetailPage: React.FC = () => {
  const { worldId, continentId } = useParams();
  const [continent, setContinent] = useState<Continent | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!worldId || !continentId) return;
    fetch(`/worlds/${worldId}/world.yaml`)
      .then((res) => res.text())
      .then((text) => {
        const data = yaml.load(text) as any;
        const found = data?.continents?.find(
          (c: any) => c.name.toLowerCase() === continentId.toLowerCase()
        );
        setContinent(found);
      })
      .catch((err) => {
        console.error("Failed to load continent:", err);
      });
  }, [worldId, continentId]);

  if (!continent || !worldId) return null;

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
        imagePath={`/worlds/${worldId}/${continent.image_path}`}
        description={continent.description}
        childrenTitle="Cities"
        childrenItems={continent.cities}
        breadcrumbLinks={[
            { label: "Worlds", href: "/" },
            { label: worldId, href: `/world/${worldId}` },
            { label: continent.name }, // current page, no href
        ]}
        />
    </>
  );
};
