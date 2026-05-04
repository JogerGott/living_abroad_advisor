import { Router } from 'express';
import { getSlang } from '../controllers/slang.controller';
import { validateResource } from '../middlewares/validateResource';
import { slangQuerySchema } from '../schemas/validationSchemas';

const router = Router();

router.get('/', validateResource(slangQuerySchema), getSlang);

export default router;
