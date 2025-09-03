// App.tsx
import React, { useEffect } from "react";
import { Container } from "@mui/material";
import { Routes, Route } from "react-router-dom";
import { WorldListPage } from "./views/WorldListPage";
import { WorldDetailPage } from "./views/WorldDetailPage";
import { ContinentDetailPage } from "./views/ContinentDetailPage";
import { OceanDetailPage } from "./views/OceanDetailPage";
import { RegionDetailPage } from "./views/RegionDetailPage";
import { CityDetailPage } from "./views/CityDetailPage";
import { logger } from "./utils/logger";

const App: React.FC = () => {
  useEffect(() => {
    logger.info("App mounted");
  }, []);

  return (
    <Container maxWidth="md" sx={{ paddingTop: 4 }}>
      <Routes>
        <Route path="/" element={<WorldListPage />} />
        <Route path="/worlds/:worldId" element={<WorldDetailPage />} />
        <Route
          path="/worlds/:worldId/continents/:continentId"
          element={<ContinentDetailPage />}
        />
        <Route
          path="/worlds/:worldId/oceans/:oceanId"
          element={<OceanDetailPage />}
        />
        <Route
          path="/worlds/:worldId/continents/:continentId/regions/:regionId"
          element={<RegionDetailPage />}
        />
        <Route
          path="/worlds/:worldId/continents/:continentId/cities/:cityId"
          element={<CityDetailPage />}
        />
      </Routes>
    </Container>
  );
};

export default App;

