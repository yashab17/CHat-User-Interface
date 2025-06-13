import { Router } from 'express';
import { QueryController } from '../controllers/queryController';

const router = Router();
const queryController = new QueryController();

router.post('/query', queryController.handleQuery.bind(queryController));

export default router;