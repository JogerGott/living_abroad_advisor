import { Router, Request, Response } from 'express';
import { globalSearch } from '../controllers/search.controller';
import { validateResource } from '../middlewares/validateResource';
import { searchQuerySchema } from '../schemas/validationSchemas';

const router = Router();

router.get('/', validateResource(searchQuerySchema), globalSearch);

// Stub for analytics
router.post('/analytics/pageview', (req: Request, res: Response) => {
  return res.status(204).send();
});

export default router;
