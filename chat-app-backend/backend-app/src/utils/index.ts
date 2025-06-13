export const logError = (error: Error): void => {
    console.error(`[ERROR] ${new Date().toISOString()}: ${error.message}`);
};

export const logInfo = (message: string): void => {
    console.log(`[INFO] ${new Date().toISOString()}: ${message}`);
};

export const handleResponse = (res: any, data: any, statusCode: number = 200): void => {
    res.status(statusCode).json(data);
};

export const handleErrorResponse = (res: any, error: Error, statusCode: number = 500): void => {
    logError(error);
    res.status(statusCode).json({ message: error.message });
};