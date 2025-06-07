// === Updated BreadcrumbNav.jsx ===
import { Breadcrumbs, Link, Typography } from '@mui/material';
import { Link as RouterLink, useLocation, useParams } from 'react-router-dom';
import { continents } from '../data/continents';
import { regions } from '../data/regions';
import { localities } from '../data/localities';
import { structures } from '../data/structures';
import { sites } from '../data/sites';
import { worldData } from '../data/worldData';

export function BreadcrumbNav() {
  const location = useLocation();
  const { id } = useParams();

  const pathParts = location.pathname.split('/').filter(Boolean);
  let crumbs = [];

  const worldLabel = worldData.name || 'World';

  if (pathParts.length === 0) {
    crumbs = [{ label: worldLabel, to: '/' }];
  } else if (pathParts[0] === 'continent') {
    const continent = continents.find(c => c.id === id);
    crumbs = [
      { label: worldLabel, to: '/' },
      { label: continent?.name || id, to: `/continent/${id}` }
    ];
  } else if (pathParts[0] === 'region') {
    const region = regions.find(r => r.id === id);
    const continent = continents.find(c => c.id === region?.continent_id);
    crumbs = [
      { label: worldLabel, to: '/' },
      { label: continent?.name || region?.continent_id, to: `/continent/${continent?.id}` },
      { label: region?.name || id, to: `/region/${id}` }
    ];
  } else if (pathParts[0] === 'locality') {
    const locality = localities.find(l => l.id === id);
    const region = regions.find(r => r.id === locality?.region_id);
    const continent = continents.find(c => c.id === region?.continent_id);
    crumbs = [
      { label: worldLabel, to: '/' },
      { label: continent?.name, to: `/continent/${continent?.id}` },
      { label: region?.name, to: `/region/${region?.id}` },
      { label: locality?.name || id, to: `/locality/${id}` }
    ];
  } else if (pathParts[0] === 'structure') {
    const structure = structures.find(s => s.id === id);
    const locality = localities.find(l => l.id === structure?.locality_id);
    const region = regions.find(r => r.id === locality?.region_id);
    const continent = continents.find(c => c.id === region?.continent_id);
    crumbs = [
      { label: worldLabel, to: '/' },
      { label: continent?.name, to: `/continent/${continent?.id}` },
      { label: region?.name, to: `/region/${region?.id}` },
      { label: locality?.name, to: `/locality/${locality?.id}` },
      { label: structure?.name || id, to: `/structure/${id}` }
    ];
  } else if (pathParts[0] === 'site') {
    const site = sites.find(s => s.id === id);
    const structure = structures.find(s => s.id === site?.structure_id);
    const locality = localities.find(l => l.id === structure?.locality_id);
    const region = regions.find(r => r.id === locality?.region_id);
    const continent = continents.find(c => c.id === region?.continent_id);
    crumbs = [
      { label: worldLabel, to: '/' },
      { label: continent?.name, to: `/continent/${continent?.id}` },
      { label: region?.name, to: `/region/${region?.id}` },
      { label: locality?.name, to: `/locality/${locality?.id}` },
      { label: structure?.name, to: `/structure/${structure?.id}` },
      { label: site?.name || id, to: `/site/${id}` }
    ];
  }

  return (
    <Breadcrumbs aria-label="breadcrumb" sx={{ marginBottom: 2 }}>
      {crumbs.map((crumb, i) =>
        i === crumbs.length - 1 ? (
          <Typography key={i} color="text.primary">
            {crumb.label}
          </Typography>
        ) : (
          <Link
            key={i}
            component={RouterLink}
            underline="hover"
            color="inherit"
            to={crumb.to}
          >
            {crumb.label}
          </Link>
        )
      )}
    </Breadcrumbs>
  );
}