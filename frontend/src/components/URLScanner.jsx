import { useState } from 'react';
import './URLScanner.css';

export default function URLScanner({ onScan, isLoading }) {
    const [url, setUrl] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        // Validation
        if (!url.trim()) {
            setError('Please enter a URL');
            return;
        }

        onScan(url.trim());
    };

    const handleClear = () => {
        setUrl('');
        setError('');
    };

    return (
        <div className="scanner-container fade-in">
            <div className="scanner-header">
                <div className="icon-wrapper">
                    <svg className="shield-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                </div>
                <div className="header-text">
                    <h1>Phishing URL Detector</h1>
                    <p className="subtitle">AI-powered protection against malicious links</p>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="scanner-form">
                <div className="input-group">
                    <input
                        type="text"
                        className="input url-input"
                        placeholder="Enter URL to scan (e.g., https://example.com)"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        disabled={isLoading}
                    />
                    {url && !isLoading && (
                        <button
                            type="button"
                            className="clear-btn"
                            onClick={handleClear}
                            aria-label="Clear"
                        >
                            ✕
                        </button>
                    )}
                </div>

                {error && (
                    <div className="error-message fade-in">
                        <svg viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    className="btn btn-primary scan-btn"
                    disabled={isLoading}
                >
                    {isLoading ? (
                        <>
                            <div className="spinner spin"></div>
                            Scanning...
                        </>
                    ) : (
                        <>
                            <svg viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                            </svg>
                            Scan URL
                        </>
                    )}
                </button>
            </form>

            <div className="quick-tips">
                <h3>🔍 Quick Tips</h3>
                <ul>
                    <li>Check suspicious emails and messages</li>
                    <li>Verify links before clicking</li>
                    <li>Look for HTTPS and correct domain spelling</li>
                </ul>
            </div>
        </div>
    );
}
