import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { WorldListPage } from '../views/WorldListPage';

describe('WorldListPage', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      json: async () => [],
    }) as any);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('renders heading', async () => {
    render(
      <MemoryRouter>
        <WorldListPage />
      </MemoryRouter>
    );

    expect(screen.getByText(/choose a world/i)).toBeInTheDocument();
    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  });
});
