import { useParams } from 'react-router-dom';
import { HierarchyView } from '../components/HierarchyView';
import { localities } from '../data/localities';
import { structures } from '../data/structures';
import { LocalityCard } from '../components/LocalityCard';

export function LocalityView() {
  const { id } = useParams();
  const locality = localities.find(l => l.id === id);
  const childStructures = structures.filter(s => s.locality_id === id);

  return (
    <HierarchyView
      parent={LocalityCard}
      parentData={locality}
      childLabel="Structures"
      children={childStructures}
      childLink={(s) => `/structure/${s.id}`}
    />
  );
}