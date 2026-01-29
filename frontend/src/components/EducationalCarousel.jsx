import { useState } from 'react';
import './EducationalCarousel.css';

export default function EducationalCarousel() {
    const [currentSlide, setCurrentSlide] = useState(0);

    const tips = [
        {
            icon: '🔍',
            title: 'Check the URL Carefully',
            description: 'Look for misspellings, extra characters, or unusual domains. Legitimate sites use their official domain names.',
            example: '❌ paypa1.com vs ✅ paypal.com'
        },
        {
            icon: '🔒',
            title: 'Look for HTTPS',
            description: 'Secure websites use HTTPS (padlock icon). However, phishing sites can also have HTTPS, so check the domain too!',
            example: 'HTTPS ≠ Always Safe'
        },
        {
            icon: '⚠️',
            title: 'Beware of Urgency',
            description: 'Phishing emails create panic with urgent messages like "Account suspended!" or "Verify now!" to make you act quickly.',
            example: 'Take time to verify before clicking'
        },
        {
            icon: '📧',
            title: 'Verify the Sender',
            description: 'Check the sender\'s email address carefully. Scammers use addresses that look similar to legitimate ones.',
            example: 'support@paypa1-secure.com ≠ Real PayPal'
        },
        {
            icon: '🎣',
            title: 'Hover Before Clicking',
            description: 'Hover over links to see the actual URL before clicking. The displayed text might be different from the real destination.',
            example: 'Display: "paypal.com" → Real: "phishing-site.com"'
        },
        {
            icon: '🛡️',
            title: 'Use This Tool!',
            description: 'When in doubt, paste the URL here and let our AI analyze it for phishing indicators. Better safe than sorry!',
            example: 'Free, instant, and accurate detection'
        }
    ];

    const nextSlide = () => {
        setCurrentSlide((prev) => (prev + 1) % tips.length);
    };

    const prevSlide = () => {
        setCurrentSlide((prev) => (prev - 1 + tips.length) % tips.length);
    };

    return (
        <div className="edu-carousel-container fade-in">
            <h2>💡 Stay Safe Online</h2>

            <div className="carousel">
                <button className="carousel-btn prev" onClick={prevSlide} aria-label="Previous tip">
                    ‹
                </button>

                <div className="carousel-content">
                    <div className="tip-icon">{tips[currentSlide].icon}</div>
                    <h3>{tips[currentSlide].title}</h3>
                    <p className="tip-description">{tips[currentSlide].description}</p>
                    <div className="tip-example">{tips[currentSlide].example}</div>
                </div>

                <button className="carousel-btn next" onClick={nextSlide} aria-label="Next tip">
                    ›
                </button>
            </div>

            <div className="carousel-dots">
                {tips.map((_, index) => (
                    <button
                        key={index}
                        className={`dot ${index === currentSlide ? 'active' : ''}`}
                        onClick={() => setCurrentSlide(index)}
                        aria-label={`Go to tip ${index + 1}`}
                    />
                ))}
            </div>

            <div className="carousel-counter">
                {currentSlide + 1} / {tips.length}
            </div>
        </div>
    );
}
