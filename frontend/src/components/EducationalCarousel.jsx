import { useState } from 'react';
import './EducationalCarousel.css';

export default function EducationalCarousel() {
    const [currentSlide, setCurrentSlide] = useState(0);

    const tips = [
        {
            icon: <svg viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" /></svg>,
            title: 'Check the URL Carefully',
            description: 'Look for misspellings, extra characters, or unusual domains. Legitimate sites use their official domain names.',
            example: '❌ paypa1.com vs ✅ paypal.com'
        },
        {
            icon: <svg viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" /></svg>,
            title: 'Look for HTTPS',
            description: 'Secure websites use HTTPS (padlock icon). However, phishing sites can also have HTTPS, so check the domain too!',
            example: 'HTTPS ≠ Always Safe'
        },
        {
            icon: <svg viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>,
            title: 'Beware of Urgency',
            description: 'Phishing emails create panic with urgent messages like "Account suspended!" or "Verify now!" to make you act quickly.',
            example: 'Take time to verify before clicking'
        },
        {
            icon: <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" /><path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" /></svg>,
            title: 'Verify the Sender',
            description: 'Check the sender\'s email address carefully. Scammers use addresses that look similar to legitimate ones.',
            example: 'support@paypa1-secure.com ≠ Real PayPal'
        },
        {
            icon: <svg viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clipRule="evenodd" /></svg>,
            title: 'Hover Before Clicking',
            description: 'Hover over links to see the actual URL before clicking. The displayed text might be different from the real destination.',
            example: 'Display: "paypal.com" → Real: "phishing-site.com"'
        },
        {
            icon: <svg viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>,
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
            <h2>
                <svg viewBox="0 0 20 20" fill="currentColor" style={{ width: '24px', height: '24px', marginRight: '8px', verticalAlign: 'middle' }}>
                    <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
                </svg>
                Stay Safe Online
            </h2>

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
