import { Request, Response, NextFunction } from 'express';
import prisma from '../utils/prismaClient';
import { AppError } from '../utils/AppError';

export const getCountries = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const countries = await prisma.country.findMany();

    const formattedData = countries.map((c) => ({
      id: c.id,
      name: c.name,
      code: c.code,
      flag: c.flag_emoji,
      coordinates: {
        latitude: c.latitude,
        longitude: c.longitude,
      },
      color: c.primary_color,
    }));

    return res.status(200).json({
      success: true,
      data: formattedData,
      meta: {
        total: formattedData.length,
      },
    });
  } catch (error) {
    next(error);
  }
};

export const getCountryByCode = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { code } = req.params;
    const country = await prisma.country.findUnique({
      where: { code: code as string },
    });

    if (!country) {
      throw new AppError(`Country with code '${code}' not found`, 404, 'RESOURCE_NOT_FOUND');
    }

    return res.status(200).json({
      success: true,
      data: {
        id: country.id,
        name: country.name,
        code: country.code,
        flag: country.flag_emoji,
        coordinates: {
          latitude: country.latitude,
          longitude: country.longitude,
        },
        color: country.primary_color,
      },
    });
  } catch (error) {
    next(error);
  }
};

export const getCompleteCountryByCode = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { code } = req.params;
    const country: any = await prisma.country.findUnique({
      where: { code: code as string },
      include: {
        cultureShocks: { orderBy: { display_order: 'asc' } },
        slangs: { orderBy: { display_order: 'asc' } },
        videos: { orderBy: { display_order: 'asc' } },
      },
    });

    if (!country) {
      throw new AppError(`Country with code '${code}' not found`, 404, 'RESOURCE_NOT_FOUND');
    }

    return res.status(200).json({
      success: true,
      data: {
        id: country.id,
        name: country.name,
        code: country.code,
        flag: country.flag_emoji,
        coordinates: {
          latitude: country.latitude,
          longitude: country.longitude,
        },
        color: country.primary_color,
        cultureShocks: country.cultureShocks.map((c: any) => ({
          id: c.id,
          title: c.title,
          description: c.description,
          icon: c.icon,
          imageUrl: c.image_url,
          order: c.display_order
        })),
        localSlang: country.slangs.map((s: any) => ({
          id: s.id,
          term: s.term,
          meaning: s.meaning,
          context: s.context,
          pronunciation: s.pronunciation,
          category: s.category,
          order: s.display_order
        })),
        videos: country.videos.map((v: any) => ({
          id: v.id,
          title: v.title,
          type: v.video_type,
          url: v.video_url,
          thumbnail: v.thumbnail_url,
          duration: v.duration,
          order: v.display_order
        })),
      },
    });
  } catch (error) {
    next(error);
  }
};
