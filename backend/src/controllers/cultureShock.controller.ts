import { Request, Response, NextFunction } from 'express';
import prisma from '../utils/prismaClient';

export const getCultureShocks = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { country_code, page = '1', limit = '10' } = req.query as any;
    
    let pageNum = parseInt(page, 10) || 1;
    let limitNum = Math.min(parseInt(limit, 10) || 10, 50);

    const whereClause: any = { is_active: true };
    if (country_code) {
      whereClause.country = { code: country_code };
    }

    const total = await prisma.cultureShock.count({ where: whereClause });
    const cultureShocks = await prisma.cultureShock.findMany({
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
      data: cultureShocks.map(c => ({
        id: c.id,
        country: { code: c.country.code, name: c.country.name },
        title: c.title,
        description: c.description,
        icon: c.icon,
        imageUrl: c.image_url,
        order: c.display_order
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
