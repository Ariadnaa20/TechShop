document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("checkoutForm");

    form.addEventListener("submit", (e) => {
        let isValid = true;

        document.querySelectorAll(".form-group").forEach(group => {
            const input = group.querySelector("input");
            const errorMsg = group.querySelector(".error-msg");
            errorMsg.textContent = "";

            if (!input.checkValidity()) {
                isValid = false;
                input.classList.add("invalid");
                errorMsg.textContent = getErrorMessage(input);
            } else {
                input.classList.remove("invalid");
            }
        });

        if (!isValid) {
            e.preventDefault();
        }
    });

    function getErrorMessage(input) {
        if (input.validity.valueMissing) return "Aquest camp és obligatori.";
        if (input.validity.tooShort) return `Has d’introduir almenys ${input.minLength} caràcters.`;
        if (input.validity.patternMismatch) return "Format incorrecte (només lletres, números i guions baixos).";
        if (input.type === "email" && input.validity.typeMismatch) return "Introdueix un correu electrònic vàlid.";
        return "Valor no vàlid.";
    }
});
