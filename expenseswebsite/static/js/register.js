// register.js

// Grab DOM elements
const usernameField = document.querySelector("#usernameField");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const usernameFeedback = document.querySelector(".invalid_feedback");
const emailFeedback = document.querySelector(".emailFeedBackArea");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const form = document.querySelector("#registerForm");

// ------------------
// Username validation
// ------------------
usernameField.addEventListener("keyup", (e) => {
  const username = e.target.value.trim();

  usernameSuccessOutput.textContent = "";
  usernameField.classList.remove("is-invalid");
  usernameFeedback.style.display = "none";

  if (username.length > 0) {
    fetch(validateUsernameUrl, {
      body: JSON.stringify({ username }),
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          usernameFeedback.style.display = "block";
          usernameFeedback.textContent = data.username_error;
        } else {
          usernameSuccessOutput.textContent = "✅ Username is available";
        }
      });
  }
});

// ------------------
// Email validation
// ------------------
emailField.addEventListener("keyup", (e) => {
  const email = e.target.value.trim();

  emailField.classList.remove("is-invalid");
  emailFeedback.style.display = "none";

  if (email.length > 0) {
    fetch(validateEmailUrl, {
      body: JSON.stringify({ email }),
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          emailField.classList.add("is-invalid");
          emailFeedback.style.display = "block";
          emailFeedback.textContent = data.email_error;
        }
      });
  }
});

// ------------------
// Show/Hide password
// ------------------
showPasswordToggle.addEventListener("click", () => {
  if (passwordField.type === "password") {
    passwordField.type = "text";
    showPasswordToggle.textContent = "HIDE";
  } else {
    passwordField.type = "password";
    showPasswordToggle.textContent = "SHOW";
  }
});

// ------------------
// Prevent auto-refresh on submit
// ------------------
form.addEventListener("submit", (e) => {
  // Allow normal Django submit, but keep this if you want JS control:
  // e.preventDefault();
  // You could add extra validation here if needed
});
