import { Card, CardContent, Typography, Stack, Chip } from '@mui/material';

export function RegionCard({ data }) {
  const {
    name,
    description,
    government_type,
    dominant_species,
    major_languages,
    economic_focus,
    cultural_traits,
    trade_partners,
    notable_locations,
    population_estimate,
    threat_level,
    tags
  } = data;

  return (
    <Card sx={{ marginTop: 4 }}>
      <CardContent>
        <Typography variant="h4" gutterBottom>{name}</Typography>
        <Typography variant="subtitle1" color="text.secondary">{description}</Typography>

        {government_type && (
          <Typography mt={2}><strong>Government Type:</strong> {government_type}</Typography>
        )}

        {population_estimate && (
          <Typography><strong>Population:</strong> {population_estimate}</Typography>
        )}

        {threat_level && (
          <Typography><strong>Threat Level:</strong> {threat_level}</Typography>
        )}

        {dominant_species?.length > 0 && (
          <>
            <Typography mt={2}><strong>Dominant Species:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {dominant_species.map((s, i) => <Chip key={i} label={s} />)}
            </Stack>
          </>
        )}

        {major_languages?.length > 0 && (
          <>
            <Typography mt={2}><strong>Major Languages:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {major_languages.map((lang, i) => <Chip key={i} label={lang} variant="outlined" />)}
            </Stack>
          </>
        )}

        {economic_focus?.length > 0 && (
          <>
            <Typography mt={2}><strong>Economic Focus:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {economic_focus.map((econ, i) => <Chip key={i} label={econ} />)}
            </Stack>
          </>
        )}

        {cultural_traits?.length > 0 && (
          <>
            <Typography mt={2}><strong>Cultural Traits:</strong></Typography>
            <Stack direction="row" spacing={1} mt={1} flexWrap="wrap">
              {cultural_traits.map((trait, i) => <Chip key={i} label={trait} variant="outlined" />)}
            </Stack>
          </>
        )}

        {trade_partners?.length > 0 && (
          <>
            <Typography mt={2}><strong>Trade Partners:</strong></Typography>
            <ul>
              {trade_partners.map((p, i) => <li key={i}>{p}</li>)}
            </ul>
          </>
        )}

        {notable_locations?.length > 0 && (
          <>
            <Typography mt={2}><strong>Notable Locations:</strong></Typography>
            <ul>
              {notable_locations.map((loc, i) => <li key={i}>{loc}</li>)}
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
