import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  CssBaseline,
  Container,
  Breadcrumbs,
  Link,
  Card,
  CardMedia,
  CardContent,
  CardActionArea,
  Divider,
  Box,
  CircularProgress,
} from "@mui/material";
import Grid from "@mui/material/Grid"; // MUI v7 Grid
import yaml from "js-yaml";

interface Continent {
  name: string;
  image_path?: string;
  description?: string;
}

interface Ocean {
  name: string;
  image_path?: string;
  description?: string;
}

interface World {
  name: string;
  genre: string;
  description: string;
  image_path: string;
  continents: Continent[];
  oceans: Ocean[];
}

export const WorldDetailPage: React.FC = () => {
  const { worldId } = useParams();
  const [world, setWorld] = useState<World | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`/worlds/${worldId}/world.yaml`)
      .then((res) => res.text())
      .then((text) => {
        const data = yaml.load(text) as World;
        setWorld(data);
      })
      .catch((err) => {
        console.error("Failed to load world YAML:", err);
      });
  }, [worldId]);

  if (!world) {
    return (
      <Box display="flex" justifyContent="center" mt={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <>
      <CssBaseline />
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6">World Explorer</Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Breadcrumbs sx={{ mb: 2 }}>
          <Link underline="hover" color="inherit" onClick={() => navigate("/")}>
            Worlds
          </Link>
          <Typography color="text.primary">{world.name}</Typography>
        </Breadcrumbs>

        <Card sx={{ mb: 4 }}>
          <CardMedia
            component="img"
            height="320"
            image={`/worlds/${worldId}/${world.image_path}`}
            alt={world.name}
            sx={{ objectFit: "cover" }}
          />
          <CardContent>
            <Typography variant="h4">{world.name}</Typography>
            <Typography variant="subtitle1" color="text.secondary">
              {world.genre}
            </Typography>
            <Typography variant="body1" sx={{ mt: 2 }}>
              {world.description}
            </Typography>
          </CardContent>
        </Card>

        <Typography variant="h5" gutterBottom>
          Continents
        </Typography>
        <Grid container spacing={3} sx={{ mb: 6 }}>
          {world.continents.map((continent) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={continent.name}>
              <Card>
                <CardActionArea onClick={() => navigate(`/worlds/${worldId}/continents/${encodeURIComponent(continent.name)}`)}>
                  {continent.image_path && (
                    <CardMedia
                      component="img"
                      height="160"
                      image={`/worlds/${worldId}/${continent.image_path}`}
                      alt={continent.name}
                    />
                  )}
                  <CardContent>
                    <Typography variant="h6">{continent.name}</Typography>
                    <Typography variant="body2" color="text.secondary" noWrap>
                      {continent.description}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Divider sx={{ my: 4 }} />

        <Typography variant="h5" gutterBottom>
          Oceans
        </Typography>
        <Grid container spacing={3}>
          {world.oceans.map((ocean) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={ocean.name}>
              <Card>
                <CardActionArea onClick={() => navigate(`/worlds/${worldId}/oceans/${encodeURIComponent(ocean.name)}`)}>
                  {ocean.image_path && (
                    <CardMedia
                      component="img"
                      height="160"
                      image={`/worlds/${worldId}/${ocean.image_path}`}
                      alt={ocean.name}
                    />
                  )}
                  <CardContent>
                    <Typography variant="h6">{ocean.name}</Typography>
                    <Typography variant="body2" color="text.secondary" noWrap>
                      {ocean.description}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </>
  );
};
