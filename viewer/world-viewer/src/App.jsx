// === src/App.jsx ===
import { Container } from '@mui/material';
import { Routes, Route } from 'react-router-dom';
import { WorldView } from './views/WorldView';
import { ContinentView } from './views/ContinentView';
import { RegionView } from './views/RegionView';
import { LocalityView } from './views/LocalityView';
import { StructureView } from './views/StructureView';
import { SiteView } from './views/SiteView';

function App() {
  return (
    <Container maxWidth="md" sx={{ paddingTop: 4 }}>
      <Routes>
        <Route path="/" element={<WorldView />} />
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
