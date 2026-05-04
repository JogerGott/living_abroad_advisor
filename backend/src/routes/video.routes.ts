import { Router } from 'express';
import { getVideos } from '../controllers/video.controller';
import { validateResource } from '../middlewares/validateResource';
import { videoQuerySchema } from '../schemas/validationSchemas';

const router = Router();

router.get('/', validateResource(videoQuerySchema), getVideos);

export default router;
