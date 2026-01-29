import './ResultDisplay.css';

export default function ResultDisplay({ result }) {
    if (!result) return null;

    const getRiskConfig = () => {
        if (result.prediction === 'legitimate') {
            return {
                color: 'success',
                icon: '✓',
                title: 'Safe URL',
                message: 'This URL appears to be legitimate and safe to visit.',
                emoji: '🛡️'
            };
        } else if (result.risk_level === 'high') {
            return {
                color: 'danger',
                icon: '⚠',
                title: 'Phishing Detected!',
                message: 'This URL is highly suspicious. Do NOT visit or share your information.',
                emoji: '🚨'
            };
        } else if (result.risk_level === 'medium') {
            return {
                color: 'warning',
                icon: '⚠',
                title: 'Suspicious URL',
                message: 'This URL shows signs of phishing. Proceed with extreme caution.',
                emoji: '⚠️'
            };
        } else {
            return {
                color: 'warning',
                icon: '?',
                title: 'Low Risk',
                message: 'This URL shows some suspicious patterns. Be cautious.',
                emoji: '🔍'
            };
        }
    };

    const config = getRiskConfig();
    const confidencePercent = (result.confidence * 100).toFixed(1);

    return (
        <div className={`result-container fade-in result-${config.color}`}>
            <div className="result-header">
                <div className={`result-icon result-icon-${config.color}`}>
                    <span className="result-emoji">{config.emoji}</span>
                </div>
                <h2>{config.title}</h2>
                <p className="result-message">{config.message}</p>
            </div>

            <div className="result-details">
                <div className="detail-card">
                    <div className="detail-label">URL Checked</div>
                    <div className="detail-value url-value">{result.url}</div>
                </div>

                <div className="detail-row">
                    <div className="detail-card">
                        <div className="detail-label">Prediction</div>
                        <div className={`detail-value badge badge-${config.color}`}>
                            {result.prediction.toUpperCase()}
                        </div>
                    </div>

                    <div className="detail-card">
                        <div className="detail-label">Confidence</div>
                        <div className="detail-value">
                            <div className="confidence-bar-container">
                                <div
                                    className={`confidence-bar confidence-bar-${config.color}`}
                                    style={{ width: `${confidencePercent}%` }}
                                ></div>
                            </div>
                            <span className="confidence-text">{confidencePercent}%</span>
                        </div>
                    </div>
                </div>

                <div className="detail-card">
                    <div className="detail-label">Risk Level</div>
                    <div className="risk-indicator">
                        <div className={`risk-dot ${result.risk_level === 'low' ? 'active' : ''}`}></div>
                        <div className={`risk-dot ${result.risk_level === 'medium' ? 'active' : ''}`}></div>
                        <div className={`risk-dot ${result.risk_level === 'high' ? 'active' : ''}`}></div>
                        <span className="risk-label">{result.risk_level.toUpperCase()}</span>
                    </div>
                </div>
            </div>

            {!result.is_safe && (
                <div className="warning-box">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    <div>
                        <strong>Security Recommendation:</strong>
                        <p>Do not enter personal information, passwords, or payment details on this website.</p>
                    </div>
                </div>
            )}
        </div>
    );
}
