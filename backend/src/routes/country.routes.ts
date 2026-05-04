import { Router } from 'express';
import { getCountries, getCountryByCode, getCompleteCountryByCode } from '../controllers/country.controller';
import { validateResource } from '../middlewares/validateResource';
import { countryParamsSchema } from '../schemas/validationSchemas';

const router = Router();

router.get('/', getCountries);
router.get('/:code', validateResource(countryParamsSchema), getCountryByCode);
router.get('/:code/complete', validateResource(countryParamsSchema), getCompleteCountryByCode);

export default router;
