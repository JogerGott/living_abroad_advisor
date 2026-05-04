import { Request, Response, NextFunction } from 'express';
import prisma from '../utils/prismaClient';

export const getSlang = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { country_code, category, page = '1', limit = '20' } = req.query as any;

    let pageNum = parseInt(page, 10) || 1;
    let limitNum = Math.min(parseInt(limit, 10) || 20, 50);

    const whereClause: any = { is_active: true };
    if (country_code) whereClause.country = { code: country_code };
    if (category) whereClause.category = category;

    const total = await prisma.localSlang.count({ where: whereClause });
    const slangs = await prisma.localSlang.findMany({
      where: whereClause,
      include: {
        country: { select: { code: true, name: true } },
      },
      orderBy: { display_order: 'asc' },
      skip: (pageNum - 1) * limitNum,
      take: limitNum,
    });

    return res.status(200).json({
      success: true,
      data: slangs.map(s => ({
        id: s.id,
        country: { code: s.country.code, name: s.country.name },
        term: s.term,
        meaning: s.meaning,
        context: s.context,
        pronunciation: s.pronunciation,
        category: s.category,
        order: s.display_order
      })),
      meta: {
        total,
        page: pageNum,
        limit: limitNum,
        totalPages: Math.ceil(total / limitNum)
      }
    });
  } catch (error) {
    next(error);
  }
};
