import { useState } from 'react';
import Login from './Login';
import Signup from './Signup';

export default function AuthWrapper({ onAuthenticated }) {
    const [isLogin, setIsLogin] = useState(true);

    const handleLogin = (userData) => {
        // Store user data in localStorage
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('isAuthenticated', 'true');

        if (onAuthenticated) {
            onAuthenticated(userData);
        }
    };

    const handleSignup = (userData) => {
        // Store user data in localStorage
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('isAuthenticated', 'true');

        if (onAuthenticated) {
            onAuthenticated(userData);
        }
    };

    return isLogin ? (
        <Login
            onLogin={handleLogin}
            onSwitchToSignup={() => setIsLogin(false)}
        />
    ) : (
        <Signup
            onSignup={handleSignup}
            onSwitchToLogin={() => setIsLogin(true)}
        />
    );
}
