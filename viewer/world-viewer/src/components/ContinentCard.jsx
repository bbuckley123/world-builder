import { Card, CardContent, Typography, Chip, Stack } from '@mui/material';

export function ContinentCard({ data }) {
  const {
    name,
    description,
    hemisphere,
    dominant_biomes,
    notable_landmarks,
    connected_water_bodies,
    common_languages,
    dominant_governing_types,
    population_estimate,
    tags
  } = data;

  return (
    <Card sx={{ marginTop: 4 }}>
      <CardContent>
        <Typography variant="h4" gutterBottom>{name}</Typography>
        <Typography variant="subtitle1" color="text.secondary">{description}</Typography>

        {hemisphere && (
          <Typography mt={2}><strong>Hemisphere:</strong> {hemisphere}</Typography>
        )}

        {population_estimate && (
          <Typography><strong>Population:</strong> {population_estimate}</Typography>
        )}

        {dominant_biomes?.length > 0 && (
          <>
            <Typography mt={2}><strong>Dominant Biomes:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {dominant_biomes.map((biome, i) => <Chip key={i} label={biome} />)}
            </Stack>
          </>
        )}

        {notable_landmarks?.length > 0 && (
          <>
            <Typography mt={2}><strong>Landmarks:</strong></Typography>
            <ul>
              {notable_landmarks.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          </>
        )}

        {connected_water_bodies?.length > 0 && (
          <>
            <Typography mt={2}><strong>Connected Water Bodies:</strong></Typography>
            <ul>
              {connected_water_bodies.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          </>
        )}

        {common_languages?.length > 0 && (
          <>
            <Typography mt={2}><strong>Languages:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {common_languages.map((lang, i) => <Chip key={i} label={lang} variant="outlined" />)}
            </Stack>
          </>
        )}

        {dominant_governing_types?.length > 0 && (
          <>
            <Typography mt={2}><strong>Governing Types:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {dominant_governing_types.map((gov, i) => <Chip key={i} label={gov} />)}
            </Stack>
          </>
        )}

        {tags?.length > 0 && (
          <>
            <Typography mt={2}><strong>Tags:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {tags.map((tag, i) => <Chip key={i} label={tag} variant="outlined" />)}
            </Stack>
          </>
        )}
      </CardContent>
    </Card>
  );
}
