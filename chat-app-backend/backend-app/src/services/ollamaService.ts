import axios from 'axios';

export class OllamaService {
    private baseUrl: string;

    constructor() {
        this.baseUrl = 'http://ollama-server-url'; // Replace with actual Ollama server URL
    }

    public async sendQuery(query: string): Promise<any> {
        try {
            const response = await axios.post(`${this.baseUrl}/query`, { query });
            return response.data;
        } catch (error) {
            throw new Error(`Error communicating with Ollama server: ${error.message}`);
        }
    }
}