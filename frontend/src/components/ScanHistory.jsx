import { useState } from 'react';
import './ScanHistory.css';

export default function ScanHistory({ history, onClearHistory }) {
    const [isExpanded, setIsExpanded] = useState(false);
    const ITEMS_TO_SHOW = 5;

    const clearHistory = () => {
        if (onClearHistory) {
            onClearHistory();
        }
    };

    const displayedHistory = isExpanded ? history.slice(0, 20) : history.slice(0, ITEMS_TO_SHOW);
    const hasMore = history.length > ITEMS_TO_SHOW;

    if (history.length === 0) {
        return (
            <div className="history-container">
                <h3>
                    <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '18px', height: '18px', marginRight: '8px' }}>
                        <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                        <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                    </svg>
                    Scan History
                </h3>
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
                <h3>
                    <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '18px', height: '18px', marginRight: '8px' }}>
                        <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                        <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                    </svg>
                    Scan History
                    <span className="history-count">({history.length})</span>
                </h3>
                <button className="btn-clear-history" onClick={clearHistory}>
                    Clear All
                </button>
            </div>

            <div className="history-list">
                {displayedHistory.map((item, index) => (
                    <div key={index} className={`history-item history-item-${item.prediction}`}>
                        <div className="history-icon">
                            {item.prediction === 'legitimate' ? (
                                <svg viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                            ) : (
                                <svg viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                </svg>
                            )}
                        </div>
                        <div className="history-content">
                            <div className="history-url">{item.url}</div>
                            <div className="history-meta">
                                <span className={`history-badge badge-${item.prediction}`}>
                                    {item.prediction}
                                </span>
                                <span className="history-confidence">
                                    {(item.confidence * 100).toFixed(0)}%
                                </span>
                                <span className="history-time">
                                    {new Date(item.timestamp).toLocaleTimeString()}
                                </span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {hasMore && (
                <button
                    className="btn-toggle-history"
                    onClick={() => setIsExpanded(!isExpanded)}
                >
                    {isExpanded ? (
                        <>
                            <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '14px', height: '14px', marginRight: '6px' }}>
                                <path fillRule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clipRule="evenodd" />
                            </svg>
                            Show Less
                        </>
                    ) : (
                        <>
                            <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '14px', height: '14px', marginRight: '6px' }}>
                                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                            Show More ({history.length - ITEMS_TO_SHOW} more)
                        </>
                    )}
                </button>
            )}
        </div>
    );
}
