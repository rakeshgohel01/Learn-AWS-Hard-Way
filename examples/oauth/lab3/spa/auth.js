// Configuration
const config = {
    userPoolId: 'us-east-1_PIalTPDoP',
    clientId: '6i7jgte399fvrfm3eea44qnfgp',
    domain: 'oauth-lab2-920372995331-domain.auth.us-east-1.amazoncognito.com',
    region: 'us-east-1',
    redirectUri: 'http://localhost:8080/callback',
    scope: 'openid profile email'
};

// Generate a random string for state
function generateState() {
    const array = new Uint32Array(28);
    window.crypto.getRandomValues(array);
    return Array.from(array, dec => ('0' + dec.toString(16)).substr(-2)).join('');
}

// Generate code verifier
function generateCodeVerifier() {
    const array = new Uint32Array(32);
    window.crypto.getRandomValues(array);
    return Array.from(array, dec => ('0' + dec.toString(16)).substr(-2)).join('');
}

// Generate code challenge from verifier
async function generateCodeChallenge(codeVerifier) {
    const encoder = new TextEncoder();
    const data = encoder.encode(codeVerifier);
    const digest = await window.crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode(...new Uint8Array(digest)))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=/g, '');
}

// Initialize login
async function login() {
    const state = generateState();
    const codeVerifier = generateCodeVerifier();
    const codeChallenge = await generateCodeChallenge(codeVerifier);

    // Store the state and code verifier
    sessionStorage.setItem('pkce_state', state);
    sessionStorage.setItem('pkce_code_verifier', codeVerifier);

    // Build the authorization URL
    const authUrl = new URL('oauth2/authorize', `https://${config.domain}`);
    const params = {
        client_id: config.clientId,
        response_type: 'code',
        scope: config.scope,
        redirect_uri: config.redirectUri,
        state: state,
        code_challenge_method: 'S256',
        code_challenge: codeChallenge
    };

    authUrl.search = new URLSearchParams(params).toString();
    window.location.href = authUrl.toString();
}

// Handle the callback
async function handleCallback() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state');
    const storedState = sessionStorage.getItem('pkce_state');
    const codeVerifier = sessionStorage.getItem('pkce_code_verifier');

    if (state !== storedState) {
        throw new Error('State mismatch');
    }

    // Exchange code for tokens
    const tokenUrl = new URL('oauth2/token', `https://${config.domain}`);
    const params = new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: config.clientId,
        code: code,
        redirect_uri: config.redirectUri,
        code_verifier: codeVerifier
    });

    try {
        const response = await fetch(tokenUrl.toString(), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: params
        });

        if (!response.ok) {
            const errorData = await response.text();
            console.error('Token exchange error:', {
                status: response.status,
                statusText: response.statusText,
                error: errorData
            });
            throw new Error(`Token exchange failed: ${errorData}`);
        }

        const data = await response.json();
        if (data.access_token) {
            sessionStorage.setItem('access_token', data.access_token);
            await getUserInfo(data.access_token);
        }
    } catch (error) {
        console.error('Error exchanging code for tokens:', error);
    }

    // Clean up PKCE session storage items
    sessionStorage.removeItem('pkce_state');
    sessionStorage.removeItem('pkce_code_verifier');
}

// Get user info using the access token
async function getUserInfo(accessToken) {
    try {
        const userInfoUrl = new URL('oauth2/userInfo', `https://${config.domain}`);
        const response = await fetch(userInfoUrl.toString(), {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        const userData = await response.json();

        document.getElementById('login-section').style.display = 'none';
        document.getElementById('user-info').style.display = 'block';
        document.getElementById('user-data').textContent = JSON.stringify(userData, null, 2);
    } catch (error) {
        console.error('Error getting user info:', error);
    }
}

// Logout function
function logout() {
    const logoutUrl = new URL('logout', `https://${config.domain}`);
    const params = {
        client_id: config.clientId,
        logout_uri: 'http://localhost:8080'
    };
    logoutUrl.search = new URLSearchParams(params).toString();

    // Clear session storage
    sessionStorage.clear();

    // Redirect to Cognito logout URL
    window.location.href = logoutUrl.toString();
}

// Check URL for authorization code on page load
window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('code')) {
        handleCallback();
    }
};
