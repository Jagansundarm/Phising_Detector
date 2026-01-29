/**
 * API Client for Phishing Detection Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export class PhishingAPI {
    /**
     * Check if a URL is phishing or legitimate
     * @param {string} url - URL to check
     * @returns {Promise<Object>} Prediction result
     */
    static async checkURL(url) {
        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'API request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Health check
     * @returns {Promise<Object>} Health status
     */
    static async healthCheck() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'offline' };
        }
    }
}
