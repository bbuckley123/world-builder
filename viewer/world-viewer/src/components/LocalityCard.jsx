import { Card, CardContent, Typography, Stack, Chip } from '@mui/material';

export function LocalityCard({ data }) {
  const {
    name,
    description,
    category,
    dominant_inhabitants,
    points_of_interest,
    population_estimate,
    tags
  } = data;

  return (
    <Card sx={{ marginTop: 4 }}>
      <CardContent>
        <Typography variant="h4" gutterBottom>{name}</Typography>
        <Typography variant="subtitle1" color="text.secondary">{description}</Typography>
        <Typography mt={2}><strong>Category:</strong> {category}</Typography>
        <Typography><strong>Population:</strong> {population_estimate}</Typography>

        {dominant_inhabitants?.length > 0 && (
          <>
            <Typography mt={2}><strong>Inhabitants:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {dominant_inhabitants.map((inh, i) => <Chip key={i} label={inh} />)}
            </Stack>
          </>
        )}

        {points_of_interest?.length > 0 && (
          <>
            <Typography mt={2}><strong>Points of Interest:</strong></Typography>
            <ul>
              {points_of_interest.map((poi, i) => <li key={i}>{poi}</li>)}
            </ul>
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
