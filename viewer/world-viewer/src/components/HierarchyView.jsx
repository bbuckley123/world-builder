import { useNavigate } from 'react-router-dom';
import { BreadcrumbNav } from './BreadcrumbNav';
import { Typography } from '@mui/material';

export function HierarchyView({ parent: ParentCard, parentData, childLabel, children, childLink }) {
  const navigate = useNavigate();

  if (!parentData) return <p>Not found.</p>;

  return (
    <>
      <BreadcrumbNav />
      <ParentCard data={parentData} />

      {children?.length > 0 && (
        <>
          <Typography variant="h6" sx={{ mt: 4 }}>{childLabel}</Typography>
          <ul>
            {children.map(child => (
              <li key={child.id}>
                <a href="#" onClick={() => navigate(childLink(child))}>
                  {child.name}
                </a>
              </li>
            ))}
          </ul>
        </>
      )}
    </>
  );
}
