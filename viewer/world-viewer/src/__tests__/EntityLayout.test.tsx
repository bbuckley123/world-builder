import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import EntityLayout from '../components/EntityLayout';

describe('EntityLayout', () => {
  it('renders title and child items', () => {
    render(
      <EntityLayout
        worldId="world"
        title="Test Title"
        childrenTitle="Children"
        childrenItems={[{ name: 'Child 1', description: 'A child' }]}
      />
    );

    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(screen.getByText('Child 1')).toBeInTheDocument();
  });
});
