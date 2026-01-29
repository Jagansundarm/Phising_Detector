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
            case 'high': return '🚨';
            case 'medium': return '⚠️';
            case 'positive': return '✅';
            default: return 'ℹ️';
        }
    };

    return (
        <div className="advanced-result-display fade-in">
            {/* Main Result Card */}
            <div className={`result-card ${result.is_safe ? 'safe' : 'phishing'}`}>
                <div className="result-header">
                    <div className="result-icon">
                        {result.is_safe ? '🛡️' : '⚠️'}
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
                    {loading ? '🔄 Loading...' : showExplanation ? '📊 Hide Details' : '🔍 Show Detailed Analysis'}
                </button>
            </div>

            {/* Detailed Explanation */}
            {showExplanation && explanation && (
                <div className="explanation-panel fade-in">
                    <h3>🔬 Detailed Analysis</h3>

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
                        <h4>📊 Feature Analysis (20 Features)</h4>
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
