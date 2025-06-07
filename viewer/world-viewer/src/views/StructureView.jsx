import { useParams } from 'react-router-dom';
import { HierarchyView } from '../components/HierarchyView';
import { structures } from '../data/structures';
import { sites } from '../data/sites';
import { StructureCard } from '../components/StructureCard';

export function StructureView() {
  const { id } = useParams();
  const structure = structures.find(s => s.id === id);
  const childSites = sites.filter(s => s.structure_id === id);

  return (
    <HierarchyView
      parent={StructureCard}
      parentData={structure}
      childLabel="Sites"
      children={childSites}
      childLink={(site) => `/site/${site.id}`}
    />
  );
}
