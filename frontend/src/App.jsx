import { useState, useEffect } from 'react';
import './App.css';
import URLScanner from './components/URLScanner';
import AdvancedResultDisplay from './components/AdvancedResultDisplay';
import ScanHistory from './components/ScanHistory';
import FeatureHighlights from './components/FeatureHighlights';
import EducationalCarousel from './components/EducationalCarousel';
import AuthWrapper from './components/AuthWrapper';

function App() {
    const [result, setResult] = useState(null);
    const [history, setHistory] = useState(() => {
        const saved = localStorage.getItem('scanHistory');
        return saved ? JSON.parse(saved) : [];
    });
    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        return localStorage.getItem('isAuthenticated') === 'true';
    });
    const [user, setUser] = useState(() => {
        const saved = localStorage.getItem('user');
        return saved ? JSON.parse(saved) : null;
    });

    const handleAuthenticated = (userData) => {
        setIsAuthenticated(true);
        setUser(userData);
    };

    const handleLogout = () => {
        setIsAuthenticated(false);
        setUser(null);
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('user');
    };

    const handleScanComplete = (scanResult) => {
        setResult(scanResult);

        // Add to history
        const newHistory = [
            {
                ...scanResult,
                timestamp: new Date().toISOString()
            },
            ...history.slice(0, 49) // Keep last 50
        ];

        setHistory(newHistory);
        localStorage.setItem('scanHistory', JSON.stringify(newHistory));
    };

    const handleClearHistory = () => {
        setHistory([]);
        localStorage.removeItem('scanHistory');
    };

    // Show login/signup if not authenticated
    if (!isAuthenticated) {
        return <AuthWrapper onAuthenticated={handleAuthenticated} />;
    }

    return (
        <div className="app">
            <div className="container">
                <header className="header">
                    <div className="header-top">
                        <div className="logo">
                            <svg className="shield-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                            <h1>PhishGuard</h1>
                        </div>
                        <div className="user-menu">
                            <div className="user-info">
                                <svg viewBox="0 0 20 20" fill="currentColor" className="user-avatar">
                                    <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                                </svg>
                                <span className="user-name">{user?.fullName || user?.email || 'User'}</span>
                            </div>
                            <button className="logout-btn" onClick={handleLogout}>
                                <svg viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 001 1h12a1 1 0 001-1V4a1 1 0 00-1-1H3zm11 4.414l-4.293 4.293a1 1 0 01-1.414-1.414L11.586 7H6a1 1 0 110-2h5.586L8.293 1.707a1 1 0 011.414-1.414L14 4.586l-4.293 4.293a1 1 0 01-1.414-1.414L11.586 9H6a1 1 0 010-2h8a1 1 0 011 1v8a1 1 0 11-2 0V7.414z" clipRule="evenodd" />
                                </svg>
                                Logout
                            </button>
                        </div>
                    </div>
                    <p className="tagline">AI-Powered Protection Against Phishing Attacks</p>
                </header>

                {/* Feature Highlights */}
                <FeatureHighlights />

                {/* Main Scanner */}
                <URLScanner onScanComplete={handleScanComplete} />

                {/* Advanced Result Display */}
                {result && <AdvancedResultDisplay result={result} />}

                {/* Educational Carousel */}
                <EducationalCarousel />

                {/* Scan History */}
                <ScanHistory
                    history={history}
                    onClearHistory={handleClearHistory}
                />

                <footer className="footer">
                    <div className="footer-content">
                        <p className="footer-tagline">
                            <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '16px', height: '16px', marginRight: '6px', verticalAlign: 'middle' }}>
                                <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            <strong>PhishGuard</strong> - Protecting users with AI-powered security
                        </p>
                        <p className="footer-privacy">
                            <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '16px', height: '16px', marginRight: '6px', verticalAlign: 'middle' }}>
                                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                            </svg>
                            Privacy-focused: URLs are analyzed in real-time and never stored on our servers
                        </p>
                        <div className="footer-links">
                            <a href="#how-it-works">How It Works</a>
                            <span>•</span>
                            <a href="#privacy">Privacy Policy</a>
                            <span>•</span>
                            <a href="#api-docs">API Documentation</a>
                            <span>•</span>
                            <a href="https://github.com" target="_blank" rel="noopener noreferrer">
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
                                </svg>
                                GitHub
                            </a>
                        </div>
                        <p className="footer-copyright">
                            Built with React, FastAPI, and LightGBM • © 2026
                        </p>
                    </div>
                </footer>
            </div>
        </div>
    );
}

export default App;

