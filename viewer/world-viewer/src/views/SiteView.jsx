import { useParams } from 'react-router-dom';
import { sites } from '../data/sites';
import { SiteCard } from '../components/SiteCard';
import { BreadcrumbNav } from '../components/BreadcrumbNav';

export function SiteView() {
  const { id } = useParams();
  const site = sites.find(s => s.id === id);

  return site ? (
    <>
      <BreadcrumbNav />
      <SiteCard data={site} />
    </>
  ) : <p>Site not found.</p>;
}
