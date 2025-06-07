import { Card, CardContent, Typography, Stack, Chip, CardMedia } from '@mui/material';

export function WorldCard({ data }) {
  const {
    name,
    description,
    creation_myth,
    dominant_technology_level,
    magic_presence,
    gravity,
    climate_summary,
    climate_features,
    hemispheres,
    notable_features,
    tags,
    image_url
  } = data;

  return (
    <Card sx={{ marginTop: 4 }}>
      {image_url && (
        <CardMedia
          component="img"
          image={image_url}
          alt={name}
          sx={{ maxHeight: 250, objectFit: 'cover' }}
        />
      )}
      <CardContent>
        <Typography variant="h3" gutterBottom>{name}</Typography>
        <Typography variant="subtitle1" color="text.secondary">{description}</Typography>

        <Typography mt={2}><strong>Creation Myth:</strong> {creation_myth}</Typography>
        <Typography><strong>Technology Level:</strong> {dominant_technology_level}</Typography>
        <Typography><strong>Magic Presence:</strong> {magic_presence}</Typography>
        <Typography><strong>Gravity:</strong> {gravity}</Typography>
        <Typography><strong>Climate Summary:</strong> {climate_summary}</Typography>

        {climate_features?.length > 0 && (
          <>
            <Typography mt={2}><strong>Climate Features:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {climate_features.map((f, i) => <Chip key={i} label={f} />)}
            </Stack>
          </>
        )}

        <Typography mt={2}><strong>Hemispheres:</strong> {hemispheres.join(', ')}</Typography>

        <Typography mt={2}><strong>Notable Features:</strong></Typography>
        <ul>
          {notable_features.map((feat, i) => <li key={i}>{feat}</li>)}
        </ul>

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
