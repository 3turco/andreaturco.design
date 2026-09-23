import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Collezione lavori — bilingue, organizzata per lingua nel filesystem.
// I file vivono in src/content/work/{it,en}/*.md.
// L'id include la lingua nel prefisso (es. "it/admiral-pay").
const work = defineCollection({
  loader: glob({ pattern: '{it,en}/**/*.{md,mdx}', base: './src/content/work' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    year: z.number(),
    role: z.string(),
    tags: z.array(z.string()),
    sector: z.string().optional(),
    cover: z.string().optional(),
    gallery: z.array(z.string()).optional(),
    // Immagini narrative del case study, con caption opzionale e posizione tra sezioni.
    // `after` = nome della sezione markdown (h2) dopo la quale mostrarle. Es. "contesto".
    images: z.array(z.object({
      src: z.string(),
      alt: z.string(),
      caption: z.string().optional(),
      after: z.string().optional(),
    })).optional(),
    client: z.string().optional(),
    link: z.string().url().optional(),
    nda: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

// Collezione blog/journal — bilingue con stessa strategia
const blog = defineCollection({
  loader: glob({ pattern: '{it,en}/**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    tags: z.array(z.string()).default([]),
    cover: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { work, blog };
