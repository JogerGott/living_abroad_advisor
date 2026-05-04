import "dotenv/config";
import app from './app';
import { logger } from './utils/logger';
import prisma from './utils/prismaClient';

const PORT = process.env.PORT || 3000;

async function bootstrap() {
  try {
    // Database check
    await prisma.$connect();
    logger.info('Database connected successfully');

    const server = app.listen(PORT, () => {
      logger.info(`Server is running on http://localhost:${PORT}`);
      logger.info(`Static screens served at http://localhost:${PORT}/Home.html`);
    });

    // Graceful shutdown
    process.on('SIGTERM', () => {
      logger.info('SIGTERM received. Shutting down gracefully.');
      server.close(() => {
        prisma.$disconnect();
        process.exit(0);
      });
    });

  } catch (error) {
    logger.error('Failed to start server:', error);
    await prisma.$disconnect();
    process.exit(1);
  }
}

bootstrap();
