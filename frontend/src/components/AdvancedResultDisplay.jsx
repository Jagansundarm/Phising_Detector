import { useState } from 'react';
import axios from 'axios';
import './AdvancedResultDisplay.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function AdvancedResultDisplay({ result }) {
    const [showExplanation, setShowExplanation] = useState(false);
    const [explanation, setExplanation] = useState(null);
    const [loading, setLoading] = useState(false);

    const getExplanation = async () => {
        if (explanation) {
            setShowExplanation(!showExplanation);
            return;
        }

        setLoading(true);
        try {
            const response = await axios.post(`${API_URL}/explain`, {
                url: result.url
            });
            setExplanation(response.data);
            setShowExplanation(true);
        } catch (error) {
            console.error('Error getting explanation:', error);
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (riskLevel) => {
        switch (riskLevel) {
            case 'low': return '#10b981';
            case 'medium': return '#f59e0b';
            case 'high': return '#ef4444';
            default: return '#6b7280';
        }
    };

    const getSeverityIcon = (severity) => {
        switch (severity) {
            case 'high':
                return <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '20px', height: '20px' }}><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>;
            case 'medium':
                return <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '20px', height: '20px' }}><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>;
            case 'positive':
                return <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '20px', height: '20px' }}><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>;
            default:
                return <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '20px', height: '20px' }}><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" /></svg>;
        }
    };

    return (
        <div className="advanced-result-display fade-in">
            {/* Main Result Card */}
            <div className={`result-card ${result.is_safe ? 'safe' : 'phishing'}`}>
                <div className="result-header">
                    <div className="result-icon">
                        {result.is_safe ? (
                            <svg viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                        ) : (
                            <svg viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                        )}
                    </div>
                    <div className="result-info">
                        <h2>{result.is_safe ? 'Safe URL' : 'Phishing Detected'}</h2>
                        <p className="url-display">{result.url}</p>
                    </div>
                </div>

                {/* Confidence Meter */}
                <div className="confidence-section">
                    <div className="confidence-header">
                        <span>Confidence Score</span>
                        <span className="confidence-value">{(result.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <div className="confidence-bar-container">
                        <div
                            className="confidence-bar"
                            style={{
                                width: `${result.confidence * 100}%`,
                                backgroundColor: getRiskColor(result.risk_level)
                            }}
                        />
                    </div>
                </div>

                {/* Risk Level Badge */}
                <div className="risk-badge-container">
                    <div
                        className="risk-badge"
                        style={{ backgroundColor: getRiskColor(result.risk_level) }}
                    >
                        Risk Level: {result.risk_level.toUpperCase()}
                    </div>
                </div>

                {/* Explanation Button */}
                <button
                    className="explain-button"
                    onClick={getExplanation}
                    disabled={loading}
                >
                    {loading ? (
                        <>
                            <svg className="spin" viewBox="0 0 20 20" fill="currentColor" style={{ width: '16px', height: '16px', marginRight: '6px' }}>
                                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                            </svg>
                            Loading...
                        </>
                    ) : showExplanation ? (
                        <>
                            <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '16px', height: '16px', marginRight: '6px' }}>
                                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                                <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                            </svg>
                            Hide Details
                        </>
                    ) : (
                        <>
                            <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '16px', height: '16px', marginRight: '6px' }}>
                                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                                <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                            </svg>
                            Show Detailed Analysis
                        </>
                    )}
                </button>
            </div>

            {/* Detailed Explanation */}
            {showExplanation && explanation && (
                <div className="explanation-panel fade-in">
                    <h3>
                        <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '20px', height: '20px', marginRight: '8px', verticalAlign: 'middle' }}>
                            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                            <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Detailed Analysis
                    </h3>

                    {/* Explanation Text */}
                    <div className="explanation-text">
                        <p>{explanation.explanation}</p>
                    </div>

                    {/* Top Indicators */}
                    {explanation.top_indicators && explanation.top_indicators.length > 0 && (
                        <div className="indicators-section">
                            <h4>Key Indicators</h4>
                            <div className="indicators-list">
                                {explanation.top_indicators.map((indicator, index) => (
                                    <div key={index} className={`indicator-card ${indicator.severity}`}>
                                        <div className="indicator-header">
                                            <span className="indicator-icon">{getSeverityIcon(indicator.severity)}</span>
                                            <span className="indicator-title">{indicator.feature}</span>
                                        </div>
                                        <div className="indicator-value">{indicator.value}</div>
                                        <div className="indicator-description">{indicator.description}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Feature Breakdown */}
                    <div className="features-section">
                        <h4>
                            <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '18px', height: '18px', marginRight: '6px', verticalAlign: 'middle' }}>
                                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                            </svg>
                            Feature Analysis (20 Features)
                        </h4>
                        <div className="features-grid">
                            {Object.entries(explanation.features).map(([name, value]) => (
                                <div key={name} className="feature-item">
                                    <span className="feature-name">{name.replace(/_/g, ' ')}</span>
                                    <span className="feature-value">{typeof value === 'number' ? value.toFixed(2) : value}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
