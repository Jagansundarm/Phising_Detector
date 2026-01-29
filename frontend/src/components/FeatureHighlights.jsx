import './FeatureHighlights.css';

export default function FeatureHighlights() {
    const features = [
        {
            icon: '🧠',
            title: 'AI-Powered Detection',
            description: 'Hybrid ML + rule-based analysis for 95%+ accuracy'
        },
        {
            icon: '⚡',
            title: 'Instant Analysis',
            description: 'Real-time URL scanning with immediate results'
        },
        {
            icon: '🔒',
            title: 'Privacy First',
            description: 'URLs analyzed securely, never stored or shared'
        },
        {
            icon: '📱',
            title: 'Works Everywhere',
            description: 'Web, mobile, and offline detection support'
        }
    ];

    return (
        <div className="feature-highlights fade-in">
            <div className="features-grid">
                {features.map((feature, index) => (
                    <div key={index} className="feature-card">
                        <div className="feature-icon">{feature.icon}</div>
                        <h3>{feature.title}</h3>
                        <p>{feature.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
