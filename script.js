document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let role = document.getElementById("role").value;

    if (name === "" || email === "" || password === "") {
        alert("All fields are required!");
        return;
    }

    // Store user role in local storage for session tracking
    localStorage.setItem("userRole", role);

    // Redirect to the respective dashboard
    redirectToDashboard(role);
});

// Function to Redirect Based on Role
function redirectToDashboard(role) {
    if (role === "admin") {
        window.location.href = "admin_dashboard.html";
    } else if (role === "trainer") {
        window.location.href = "serviceprovider_dashboard.html";
    } else {
        window.location.href = "customer_dashboard.html";
    }
}
// Logout function (clears session and redirects to Get Started page)
function logout() {
    localStorage.removeItem("userRole");
    window.location.href = "getstarted_page.html";
}

// Auto-Redirect if Not Logged In
document.addEventListener("DOMContentLoaded", function() {
    let storedRole = localStorage.getItem("userRole");
    if (!storedRole) {
        window.location.href = "registration_login_page.html"; // Redirect if no session found
    }
});
