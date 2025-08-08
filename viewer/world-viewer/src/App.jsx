// === src/App.jsx ===
import { Container } from '@mui/material';
import { Routes, Route } from 'react-router-dom';
import { WorldListPage } from './views/WorldListPage';
import { WorldDetailPage } from './views/WorldDetailPage';
import { ContinentDetailPage } from './views/ContinentDetailPage';
import { OceanDetailPage } from './views/OceanDetailPage';
import { RegionDetailPage } from './views/RegionDetailPage';
import { CityDetailPage } from './views/CityDetailPage';
import { RealmView } from './views/RealmView';
import { ContinentView } from './views/ContinentView';
import { RegionView } from './views/RegionView';
import { LocalityView } from './views/LocalityView';
import { StructureView } from './views/StructureView';
import { SiteView } from './views/SiteView';

function App() {
  return (
    <Container maxWidth="md" sx={{ paddingTop: 4 }}>
      <Routes>
        <Route path="/" element={<WorldListPage />} />
        <Route path="/worlds/:worldId" element={<WorldDetailPage />} />
        <Route path="/worlds/:worldId/continents/:continentId" element={<ContinentDetailPage />} />
        <Route path="/worlds/:worldId/oceans/:oceanId" element={<OceanDetailPage />} />
        <Route path="/worlds/:worldId/continents/:continentId/regions/:regionId" element={<RegionDetailPage />} />
        <Route path="/worlds/:worldId/continents/:continentId/cities/:cityId" element={<CityDetailPage />} />
        <Route path="/continent/:id" element={<ContinentView />} />
        <Route path="/region/:id" element={<RegionView />} />
        <Route path="/locality/:id" element={<LocalityView />} />
        <Route path="/structure/:id" element={<StructureView />} />
        <Route path="/site/:id" element={<SiteView />} />
      </Routes>
    </Container>
  );
}

export default App;
