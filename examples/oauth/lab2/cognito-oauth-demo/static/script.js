// Check if we have a token in sessionStorage
window.onload = function () {
  console.log("Page loaded, checking for access token...");
  const token = sessionStorage.getItem("access_token");
  console.log("Access token present:", !!token);
  updateUIState(token);
};

function updateUIState(token) {
  console.log("Updating UI state, token present:", !!token);
  if (token) {
    document.getElementById("loginSection").style.display = "none";
    document.getElementById("userInfo").style.display = "block";
    fetchUserInfo(token);
  } else {
    document.getElementById("loginSection").style.display = "block";
    document.getElementById("userInfo").style.display = "none";
    document.getElementById("userInfoContent").textContent = "";
  }
}

function fetchUserInfo(token) {
  console.log("Fetching user info...");
  console.log("Request URL:", window.location.origin + "/userinfo");
  console.log(
    "Authorization Header:",
    "Bearer " + token.substring(0, 10) + "..."
  );

  fetch("/userinfo", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/json",
    },
    credentials: "include",
  })
    .then((response) => {
      console.log("Response status:", response.status);
      console.log(
        "Response headers:",
        Object.fromEntries([...response.headers])
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log("User info received:", data);
      document.getElementById("userInfoContent").textContent = JSON.stringify(
        data,
        null,
        2
      );
    })
    .catch((error) => {
      console.error("Error fetching user info:", error);
      console.error("Error details:", error.message);
      sessionStorage.removeItem("access_token");
      updateUIState(null);
    });
}

function logout() {
  console.log("Logging out...");
  
  // First clear local session storage
  sessionStorage.removeItem("access_token");
  
  // Call backend to get Cognito logout URL
  fetch("/logout", {
    method: "GET",
    credentials: "include",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Redirecting to Cognito logout URL:", data.logout_url);
      // Redirect to Cognito logout URL
      window.location.href = data.logout_url;
    })
    .catch((error) => {
      console.error("Error during logout:", error);
      // Even if there's an error, update the UI
      updateUIState(null);
    });
}
