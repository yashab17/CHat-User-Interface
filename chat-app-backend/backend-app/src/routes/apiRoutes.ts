import { Router } from 'express';
import { QueryController } from '../controllers/queryController';

const router = Router();
const queryController = new QueryController();

export const setApiRoutes = (app) => {
    app.use('/api', router);

    router.post('/query', queryController.handleQuery.bind(queryController));
};