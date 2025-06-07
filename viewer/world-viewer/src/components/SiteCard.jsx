import { Card, CardContent, Typography, Stack, Chip } from '@mui/material';

export function SiteCard({ data }) {
  const { name, description, function: func, access_requirements, tags } = data;

  return (
    <Card sx={{ marginTop: 4 }}>
      <CardContent>
        <Typography variant="h4" gutterBottom>{name}</Typography>
        <Typography variant="subtitle1" color="text.secondary">{description}</Typography>
        <Typography mt={2}><strong>Function:</strong> {func}</Typography>

        {access_requirements?.length > 0 && (
          <>
            <Typography mt={2}><strong>Access Requirements:</strong></Typography>
            <ul>
              {access_requirements.map((req, i) => <li key={i}>{req}</li>)}
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
