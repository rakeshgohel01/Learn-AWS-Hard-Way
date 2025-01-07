function startLogin() {
    window.location.href = '/login';
}

// Check if we have a token in sessionStorage
window.onload = function() {
    const token = sessionStorage.getItem('access_token');
    if (token) {
        fetchUserInfo(token);
    }
};

function fetchUserInfo(token) {
    fetch('/userinfo', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loginSection').style.display = 'none';
        document.getElementById('userInfo').style.display = 'block';
        document.getElementById('userInfoContent').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
        sessionStorage.removeItem('access_token');
    });
}

function logout() {
    sessionStorage.removeItem('access_token');
    window.location.href = '/';
}
