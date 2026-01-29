import { useState, useEffect } from 'react';
import './ScanHistory.css';

export default function ScanHistory() {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        // Load history from localStorage
        const saved = localStorage.getItem('scanHistory');
        if (saved) {
            setHistory(JSON.parse(saved));
        }
    }, []);

    const clearHistory = () => {
        localStorage.removeItem('scanHistory');
        setHistory([]);
    };

    if (history.length === 0) {
        return (
            <div className="history-container">
                <h3>📜 Scan History</h3>
                <div className="empty-state">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                        <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                    </svg>
                    <p>No scans yet. Start by checking a URL above!</p>
                </div>
            </div>
        );
    }

    return (
        <div className="history-container">
            <div className="history-header">
                <h3>📜 Scan History</h3>
                <button className="btn-clear-history" onClick={clearHistory}>
                    Clear All
                </button>
            </div>

            <div className="history-list">
                {history.slice(0, 10).map((item, index) => (
                    <div key={index} className={`history-item history-item-${item.prediction}`}>
                        <div className="history-icon">
                            {item.prediction === 'legitimate' ? '✓' : '⚠'}
                        </div>
                        <div className="history-content">
                            <div className="history-url">{item.url}</div>
                            <div className="history-meta">
                                <span className={`history-badge badge-${item.prediction}`}>
                                    {item.prediction}
                                </span>
                                <span className="history-confidence">
                                    {(item.confidence * 100).toFixed(0)}% confidence
                                </span>
                                <span className="history-time">
                                    {new Date(item.timestamp).toLocaleString()}
                                </span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
