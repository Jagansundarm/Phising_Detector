/**
 * API Service for PhishGuard
 * Handles all API calls to the backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Generic API request handler
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.message || 'An error occurred');
        }

        return data;
    } catch (error) {
        if (error.message === 'Failed to fetch') {
            throw new Error('Unable to connect to server. Please check your connection.');
        }
        throw error;
    }
}

// ==================== Authentication API ====================

/**
 * Register a new user
 */
export async function registerUser(userData) {
    return apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
            email: userData.email,
            full_name: userData.fullName,
            password: userData.password,
            confirm_password: userData.confirmPassword,
            agree_to_terms: userData.agreeToTerms,
            agree_to_privacy: userData.agreeToPrivacy,
            subscribe_newsletter: userData.subscribeNewsletter || false,
        }),
    });
}

/**
 * Login user
 */
export async function loginUser(credentials) {
    const response = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
            email: credentials.email,
            password: credentials.password,
            remember_me: credentials.rememberMe || false,
        }),
    });

    // Store the token
    if (response.access_token) {
        localStorage.setItem('authToken', response.access_token);
    }

    return response;
}

/**
 * Get current user profile
 */
export async function getCurrentUser() {
    return apiRequest('/auth/me', {
        method: 'GET',
    });
}

/**
 * Update user profile
 */
export async function updateProfile(profileData) {
    return apiRequest('/auth/me', {
        method: 'PUT',
        body: JSON.stringify(profileData),
    });
}

/**
 * Logout user
 */
export async function logoutUser() {
    try {
        await apiRequest('/auth/logout', { method: 'POST' });
    } finally {
        // Always clear local storage
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        localStorage.removeItem('isAuthenticated');
    }
}

/**
 * Get user statistics
 */
export async function getUserStats() {
    return apiRequest('/auth/stats', {
        method: 'GET',
    });
}

// ==================== URL Scanning API ====================

/**
 * Scan a URL for phishing
 */
export async function scanUrl(url) {
    return apiRequest('/predict', {
        method: 'POST',
        body: JSON.stringify({ url }),
    });
}

/**
 * Get detailed explanation for a URL
 */
export async function getExplanation(url) {
    return apiRequest('/explain', {
        method: 'POST',
        body: JSON.stringify({ url }),
    });
}

/**
 * Check API health
 */
export async function checkHealth() {
    return apiRequest('/health', {
        method: 'GET',
    });
}

/**
 * Get model information
 */
export async function getModelInfo() {
    return apiRequest('/model-info', {
        method: 'GET',
    });
}

export default {
    registerUser,
    loginUser,
    getCurrentUser,
    updateProfile,
    logoutUser,
    getUserStats,
    scanUrl,
    getExplanation,
    checkHealth,
    getModelInfo,
};
