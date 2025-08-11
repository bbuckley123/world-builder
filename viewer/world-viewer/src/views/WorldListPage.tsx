import React, { useEffect, useState } from "react";
import {
  AppBar,
  Box,
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  CircularProgress,
  Container,
  CssBaseline,
  Toolbar,
  Typography,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import { useNavigate } from "react-router-dom";

// World type definition
type WorldSummary = {
  id: string;
  name: string;
  genre: string;
  description: string;
  preview: string; // e.g., "elyria/images/world.png"
};

export const WorldListPage: React.FC = () => {
  const [worlds, setWorlds] = useState<WorldSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/worlds/worlds.json")
      .then((res) => res.json())
      .then((data) => {
        setWorlds(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load worlds.json:", err);
        setLoading(false);
      });
  }, []);

  return (
    <>
      <CssBaseline />
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6">🌍 World Explorer</Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Choose a World
        </Typography>

        {loading ? (
          <Box display="flex" justifyContent="center" mt={4}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            {worlds.map((world) => (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={world.id}>
                <Card>
                  <CardActionArea onClick={() => navigate(`/worlds/${world.id}`)}>
                    <CardMedia
                      component="img"
                      height="180"
                      image={`worlds/${world.preview}`} // Static asset path
                      alt={world.name}
                      sx={{ objectFit: "cover" }}
                    />
                    <CardContent>
                      <Typography variant="h6">{world.name}</Typography>
                      <Typography variant="subtitle2" color="text.secondary">
                        {world.genre}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" noWrap>
                        {world.description}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Container>
    </>
  );
};
