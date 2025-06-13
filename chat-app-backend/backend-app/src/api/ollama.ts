import axios from 'axios';

const OLLAMA_API_URL = 'http://localhost:11434'; // Replace with your Ollama server URL

export const sendQueryToOllama = async (query: string): Promise<any> => {
    try {
        const response = await axios.post(`${OLLAMA_API_URL}/query`, { query });
        return response.data;
    } catch (error) {
        console.error('Error communicating with Ollama server:', error);
        throw new Error('Failed to get response from Ollama server');
    }
};