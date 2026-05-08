import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const progetti = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/progetti' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    year: z.number(),
    role: z.string(),
    tags: z.array(z.string()),
    cover: z.string().optional(),
    gallery: z.array(z.string()).optional(),
    client: z.string().optional(),
    link: z.string().url().optional(),
    draft: z.boolean().default(false),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    tags: z.array(z.string()).default([]),
    cover: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { progetti, blog };
