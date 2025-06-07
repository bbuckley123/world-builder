import { useParams } from 'react-router-dom';
import { HierarchyView } from '../components/HierarchyView';
import { continents } from '../data/continents';
import { regions } from '../data/regions';
import { ContinentCard } from '../components/ContinentCard';

export function ContinentView() {
  const { id } = useParams();
  const continent = continents.find(c => c.id === id);
  const childRegions = regions.filter(r => r.continent_id === id);

  return (
    <HierarchyView
      parent={ContinentCard}
      parentData={continent}
      childLabel="Regions"
      children={childRegions}
      childLink={(r) => `/region/${r.id}`}
    />
  );
}
