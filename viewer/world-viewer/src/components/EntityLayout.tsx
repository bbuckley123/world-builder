// EntityLayout.tsx
import React from "react";
import {
  Card,
  CardContent,
  CardMedia,
  Container,
  Typography,
  Breadcrumbs,
  Link,
  Grid,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

type ChildEntity = {
  name: string;
  description?: string;
  image_path?: string;
};

type Crumb = { label: string; href?: string };

type EntityLayoutProps = {
  worldId: string,
  title: string;
  subtitle?: string;
  imagePath?: string;
  description?: string;
  childrenTitle?: string;
  childrenItems?: ChildEntity[];
  breadcrumbLinks?: Crumb[]; // <-- unified name
};

const EntityLayout: React.FC<EntityLayoutProps> = ({
  worldId,
  title,
  subtitle,
  imagePath,
  description,
  childrenTitle,
  childrenItems = [],         // safe default
  breadcrumbLinks = [],       // safe default
}) => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      {breadcrumbLinks.length > 0 && (
        <Breadcrumbs sx={{ mb: 2 }}>
          {breadcrumbLinks.map((crumb, idx) =>
            crumb.href ? (
              <Link
                key={idx}
                component={RouterLink}
                underline="hover"
                color="inherit"
                to={crumb.href}     // use RouterLink "to"
              >
                {crumb.label}
              </Link>
            ) : (
              <Typography key={idx} color="text.primary">
                {crumb.label}
              </Typography>
            )
          )}
        </Breadcrumbs>
      )}

      {imagePath && (
        <Card sx={{ mb: 4 }}>
          <CardMedia
            component="img"
            height="320"
            image={imagePath}
            alt={title}
            sx={{ objectFit: "cover" }}
          />
        </Card>
      )}

      <Typography variant="h4" gutterBottom>{title}</Typography>
      {subtitle && (
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          {subtitle}
        </Typography>
      )}
      {description && (
        <Typography variant="body1" sx={{ mb: 4 }}>{description}</Typography>
      )}

      {childrenItems.length > 0 && (
        <>
          {childrenTitle && (
            <Typography variant="h5" gutterBottom>{childrenTitle}</Typography>
          )}
          <Grid container spacing={3}>
            {childrenItems.map((child) => (
              <Grid key={child.name} size={{ xs: 12, sm: 6, md: 4 }}>
                <Card>
                  {child.image_path && (
                    <CardMedia
                      component="img"
                      height="160"
                      image={`/worlds/${worldId}/${child.image_path}`}
                      alt={child.name}
                    />
                  )}
                  <CardContent>
                    <Typography variant="h6">{child.name}</Typography>
                    <Typography variant="body2" color="text.secondary" noWrap>
                      {child.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </>
      )}
    </Container>
  );
};

export default EntityLayout;
