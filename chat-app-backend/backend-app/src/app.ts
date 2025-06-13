import express from 'express';
import bodyParser from 'body-parser';
import { setApiRoutes } from './routes/apiRoutes';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

setApiRoutes(app);

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});