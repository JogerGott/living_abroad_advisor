import { Router } from 'express';
import { getCultureShocks } from '../controllers/cultureShock.controller';
import { validateResource } from '../middlewares/validateResource';
import { paginationQuerySchema } from '../schemas/validationSchemas';

const router = Router();

router.get('/', validateResource(paginationQuerySchema), getCultureShocks);

export default router;
