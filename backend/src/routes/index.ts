import { Router } from 'express';
import countryRoutes from './country.routes';
import cultureShockRoutes from './cultureShock.routes';
import slangRoutes from './slang.routes';
import videoRoutes from './video.routes';
import searchRoutes from './search.routes';

const router = Router();

router.use('/countries', countryRoutes);
router.use('/culture-shocks', cultureShockRoutes);
router.use('/slang', slangRoutes);
router.use('/videos', videoRoutes);
// global search and analytics
router.use('/', searchRoutes);

export default router;
