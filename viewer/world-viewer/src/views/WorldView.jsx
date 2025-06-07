import { HierarchyView } from '../components/HierarchyView';
import { worldData } from '../data/worldData';
import { continents } from '../data/continents';
import { WorldCard } from '../components/WorldCard';

export function WorldView() {
  const relatedContinents = continents.filter(c => c.world_id === worldData.id);

  return (
    <HierarchyView
      parent={WorldCard}
      parentData={worldData}
      childLabel="Continents"
      children={relatedContinents}
      childLink={(c) => `/continent/${c.id}`}
    />
  );
}
