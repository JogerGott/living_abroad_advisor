import { z } from 'zod';

export const countryParamsSchema = z.object({
  params: z.object({
    code: z.string().length(2).toUpperCase(),
  }),
});

export const paginationQuerySchema = z.object({
  query: z.object({
    page: z.string().regex(/^\d+$/).optional().transform(Number),
    limit: z.string().regex(/^\d+$/).optional().transform(Number),
    language: z.enum(['en', 'es']).optional().default('en'),
    country_code: z.string().length(2).toUpperCase().optional(),
  }),
});

export const slangQuerySchema = paginationQuerySchema.merge(
  z.object({
    query: z.object({
      category: z.enum(['greeting', 'food', 'expression', 'insult', 'other']).optional(),
    }).passthrough(),
  })
);

export const videoQuerySchema = paginationQuerySchema.merge(
  z.object({
    query: z.object({
      type: z.enum(['youtube', 'vimeo', 'local']).optional(),
    }).passthrough(),
  })
);

export const searchQuerySchema = z.object({
  query: z.object({
    q: z.string().min(1),
    type: z.enum(['culture_shock', 'slang', 'all']).optional().default('all'),
    country_code: z.string().length(2).toUpperCase().optional(),
    language: z.enum(['en', 'es']).optional().default('en'),
    page: z.string().regex(/^\d+$/).optional().transform(Number),
    limit: z.string().regex(/^\d+$/).optional().transform(Number),
  }),
});
