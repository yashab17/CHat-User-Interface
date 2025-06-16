// import { Request, Response } from 'express';
// import { OllamaService } from '../services/ollamaService';

// export class QueryController {
//     private ollamaService: OllamaService;

//     constructor() {
//         this.ollamaService = new OllamaService();
//     }

//     public async handleQuery(req: Request, res: Response): Promise<void> {
//         const query = req.body.query;

//         try {
//             const response = await this.ollamaService.sendQuery(query);
//             res.status(200).json({ response });
//         } catch (error) {
//             res.status(500).json({ error: 'An error occurred while processing your query.' });
//         }
//     }
// }

exports.processQuery = async (req, res) => {
  const query = req.body.query;

  // 1. Tokenize query and embed
  // 2. Search in vector DB for top-k
  // 3. Call LLM with context + query
  // 4. Return synthesized response

  res.send("Answer generated.");
};
