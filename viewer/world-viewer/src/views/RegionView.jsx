import { useParams } from 'react-router-dom';
import { HierarchyView } from '../components/HierarchyView';
import { regions } from '../data/regions';
import { localities } from '../data/localities';
import { RegionCard } from '../components/RegionCard';

export function RegionView() {
  const { id } = useParams();
  const region = regions.find(r => r.id === id);
  const childLocalities = localities.filter(l => l.region_id === id);

  return (
    <HierarchyView
      parent={RegionCard}
      parentData={region}
      childLabel="Localities"
      children={childLocalities}
      childLink={(l) => `/locality/${l.id}`}
    />
  );
}
