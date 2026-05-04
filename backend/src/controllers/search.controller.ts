import { Request, Response, NextFunction } from 'express';
import prisma from '../utils/prismaClient';

export const globalSearch = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { q, type = 'all', country_code, page = '1', limit = '10' } = req.query as any;

    let pageNum = parseInt(page, 10) || 1;
    let limitNum = Math.min(parseInt(limit, 10) || 10, 50);

    let cultureShocks: any[] = [];
    let slangs: any[] = [];

    const countryFilter = country_code ? { country: { code: country_code } } : {};

    if (type === 'all' || type === 'culture_shock') {
      cultureShocks = await prisma.cultureShock.findMany({
        where: {
          ...countryFilter,
          is_active: true,
          OR: [
            { title: { contains: q } },
            { description: { contains: q } }
          ]
        },
        include: { country: { select: { code: true, name: true } } },
        take: limitNum
      });
    }

    if (type === 'all' || type === 'slang') {
      slangs = await prisma.localSlang.findMany({
        where: {
          ...countryFilter,
          is_active: true,
          OR: [
            { term: { contains: q } },
            { meaning: { contains: q } },
            { context: { contains: q } }
          ]
        },
        include: { country: { select: { code: true, name: true } } },
        take: limitNum
      });
    }

    return res.status(200).json({
      success: true,
      data: {
        cultureShocks: cultureShocks.map(c => ({
          id: c.id,
          country: { code: c.country.code, name: c.country.name },
          title: c.title,
          description: c.description,
          icon: c.icon,
          imageUrl: c.image_url,
          order: c.display_order
        })),
        slang: slangs.map(s => ({
          id: s.id,
          country: { code: s.country.code, name: s.country.name },
          term: s.term,
          meaning: s.meaning,
          category: s.category
        }))
      },
      meta: {
        total: cultureShocks.length + slangs.length,
        query: q
      }
    });

  } catch (error) {
    next(error);
  }
};
