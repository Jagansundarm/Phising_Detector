import { useState } from 'react';
import './ThreatIntelligence.css';

export default function ThreatIntelligence() {
    const [stats] = useState({
        scansToday: Math.floor(Math.random() * 1000) + 500,
        phishingDetected: Math.floor(Math.random() * 100) + 50,
        threatsStopped: Math.floor(Math.random() * 200) + 100,
        accuracy: 95.8
    });

    const recentThreats = [
        { type: 'PayPal Phishing', count: 23, trend: 'up' },
        { type: 'Banking Scams', count: 18, trend: 'up' },
        { type: 'Crypto Fraud', count: 15, trend: 'down' },
        { type: 'Social Media', count: 12, trend: 'stable' }
    ];

    return (
        <div className="threat-intel-container fade-in">
            <h2>🔍 Live Threat Intelligence</h2>

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon">📊</div>
                    <div className="stat-value">{stats.scansToday.toLocaleString()}</div>
                    <div className="stat-label">Scans Today</div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">🚨</div>
                    <div className="stat-value">{stats.phishingDetected}</div>
                    <div className="stat-label">Threats Detected</div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">🛡️</div>
                    <div className="stat-value">{stats.threatsStopped}</div>
                    <div className="stat-label">Users Protected</div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">✨</div>
                    <div className="stat-value">{stats.accuracy}%</div>
                    <div className="stat-label">Accuracy Rate</div>
                </div>
            </div>

            <div className="recent-threats">
                <h3>🔥 Trending Threats</h3>
                <div className="threats-list">
                    {recentThreats.map((threat, index) => (
                        <div key={index} className="threat-item">
                            <div className="threat-info">
                                <span className="threat-type">{threat.type}</span>
                                <span className="threat-count">{threat.count} detected</span>
                            </div>
                            <div className={`threat-trend trend-${threat.trend}`}>
                                {threat.trend === 'up' && '↗️'}
                                {threat.trend === 'down' && '↘️'}
                                {threat.trend === 'stable' && '→'}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
