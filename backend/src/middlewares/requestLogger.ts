import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';

export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const elapsed = Date.now() - start;
    logger.info(`[${req.method}] ${req.originalUrl} - ${res.statusCode} (${elapsed}ms) - IP: ${req.ip}`);
  });

  next();
};
