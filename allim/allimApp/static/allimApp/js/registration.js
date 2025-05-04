document.addEventListener("DOMContentLoaded", function () {

    function validateField(inputId, feedbackId, minLength, message) {
        const input = document.getElementById(inputId);
        const feedback = document.getElementById(feedbackId);

        input.addEventListener("input", function () {
            const value = this.value.trim();

            if (value.length < minLength) {
                this.classList.add("is-invalid");
                this.classList.remove("is-valid");
                feedback.textContent = message;
                feedback.classList.add("text-danger");
                feedback.classList.remove("text-success");
            } else {
                this.classList.remove("is-invalid");
                this.classList.add("is-valid");
                feedback.textContent = "Looks good!";
                feedback.classList.remove("text-danger");
                feedback.classList.add("text-success");
            }
        });
    }
    validateField("passwordReg", "passwordFeedback", 8 ,"Please enter a password with a minimum of 10 characters.");
    validateField("firstName", "firstNameFeedback", 3, "First name must be at least 3 characters.");
    validateField("last_name", "lastNameFeedback", 3, "Last name must be at least 5 characters.");

    // Email validation
    const emailInput = document.getElementById("email");
    const emailFeedback = document.getElementById("emailFeedback");

    emailInput.addEventListener("input", function () {
        const value = this.value.trim().toLowerCase();

        if (
            value.endsWith("@gmail.com") ||
            value.endsWith("@outlook.com") ||
            value.endsWith("@hotmail.com")
        ) {
            this.classList.remove("is-invalid");
            this.classList.add("is-valid");
            emailFeedback.textContent = "Valid email domain";
            emailFeedback.classList.remove("text-danger");
            emailFeedback.classList.add("text-success");
        } else {
            this.classList.add("is-invalid");
            this.classList.remove("is-valid");
            emailFeedback.textContent = " Must be a valid email domain (e.g., @gmail.com, @outlook.com, @hotmail.com)";
            emailFeedback.classList.add("text-danger");
            emailFeedback.classList.remove("text-success");
        }
    });
});
