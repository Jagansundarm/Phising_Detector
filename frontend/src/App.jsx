import { useState } from 'react';
import './App.css';
import URLScanner from './components/URLScanner';
import AdvancedResultDisplay from './components/AdvancedResultDisplay';
import ScanHistory from './components/ScanHistory';
import FeatureHighlights from './components/FeatureHighlights';
import EducationalCarousel from './components/EducationalCarousel';
import ShareResults from './components/ShareResults';

function App() {
    const [result, setResult] = useState(null);
    const [history, setHistory] = useState(() => {
        const saved = localStorage.getItem('scanHistory');
        return saved ? JSON.parse(saved) : [];
    });

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

    return (
        <div className="app">
            <div className="container">
                <header className="header">
                    <div className="logo">
                        <div className="shield-icon">🛡️</div>
                        <h1>Phishing URL Detector</h1>
                    </div>
                    <p className="tagline">AI-Powered Protection Against Phishing Attacks</p>
                </header>

                {/* Feature Highlights */}
                <FeatureHighlights />

                {/* Main Scanner */}
                <URLScanner onScanComplete={handleScanComplete} />

                {/* Advanced Result Display */}
                {result && <AdvancedResultDisplay result={result} />}

                {/* Share Results */}
                {result && <ShareResults result={result} />}

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
                            🛡️ <strong>Phishing URL Detector</strong> - Protecting users with AI-powered security
                        </p>
                        <p className="footer-privacy">
                            🔒 Privacy-focused: URLs are analyzed in real-time and never stored on our servers
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
