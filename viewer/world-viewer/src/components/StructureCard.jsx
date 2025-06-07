import { Card, CardContent, Typography, Stack, Chip } from '@mui/material';

export function StructureCard({ data }) {
  const {
    name,
    description,
    category,
    origin,
    known_properties,
    tags
  } = data;

  return (
    <Card sx={{ marginTop: 4 }}>
      <CardContent>
        <Typography variant="h4" gutterBottom>{name}</Typography>
        <Typography variant="subtitle1" color="text.secondary">{description}</Typography>
        <Typography mt={2}><strong>Category:</strong> {category}</Typography>
        <Typography><strong>Origin:</strong> {origin}</Typography>

        {known_properties?.length > 0 && (
          <>
            <Typography mt={2}><strong>Properties:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {known_properties.map((prop, i) => <Chip key={i} label={prop} />)}
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