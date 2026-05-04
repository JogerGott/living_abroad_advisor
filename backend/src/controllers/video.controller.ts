import { Request, Response, NextFunction } from 'express';
import prisma from '../utils/prismaClient';

export const getVideos = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { country_code, type, page = '1', limit = '10' } = req.query as any;

    let pageNum = parseInt(page, 10) || 1;
    let limitNum = Math.min(parseInt(limit, 10) || 10, 50);

    const whereClause: any = { is_active: true };
    if (country_code) whereClause.country = { code: country_code };
    if (type) whereClause.video_type = type;

    const total = await prisma.video.count({ where: whereClause });
    const videos = await prisma.video.findMany({
      where: whereClause,
      include: { country: { select: { code: true, name: true } } },
      orderBy: { display_order: 'asc' },
      skip: (pageNum - 1) * limitNum,
      take: limitNum,
    });

    return res.status(200).json({
      success: true,
      data: videos.map(v => ({
        id: v.id,
        country: { code: v.country.code, name: v.country.name },
        title: v.title,
        type: v.video_type,
        url: v.video_url,
        thumbnail: v.thumbnail_url,
        duration: v.duration,
        order: v.display_order
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
