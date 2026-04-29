// KFUEIT Job Fair 2026 – Form Validation & Submission

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registrationForm');
    if (!form) return;

    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn?.querySelector('.btn-text');
    const btnLoading = submitBtn?.querySelector('.btn-loading');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        e.stopPropagation();

        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            const firstInvalid = form.querySelector(':invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstInvalid.focus();
            }
            return;
        }

        form.classList.add('was-validated');

        if (submitBtn && btnText && btnLoading) {
            submitBtn.disabled = true;
            btnText.classList.add('d-none');
            btnLoading.classList.remove('d-none');
        }

        form.submit();
    });

    // Phone formatting: 03XX-XXXXXXX
    const phoneInput = form.querySelector('input[name="phone"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function () {
            let val = this.value.replace(/\D/g, '').slice(0, 11);
            if (val.length > 4) {
                val = val.slice(0, 4) + '-' + val.slice(4);
            }
            this.value = val;
        });
    }

    // CNIC formatting: XXXXX-XXXXXXX-X  (fixed: was breaking at 13 chars)
    const cnicInput = form.querySelector('input[name="cnic"]');
    if (cnicInput) {
        cnicInput.addEventListener('input', function () {
            let val = this.value.replace(/\D/g, '').slice(0, 13);
            if (val.length > 12) {
                val = val.slice(0, 5) + '-' + val.slice(5, 12) + '-' + val.slice(12);
            } else if (val.length > 5) {
                val = val.slice(0, 5) + '-' + val.slice(5);
            }
            this.value = val;
        });
    }

    // GPA validation
    const gpaInput = form.querySelector('input[name="gpa"]');
    if (gpaInput) {
        gpaInput.addEventListener('blur', function () {
            const val = parseFloat(this.value);
            if (this.value && (isNaN(val) || val < 0 || val > 4)) {
                this.setCustomValidity('GPA must be between 0.00 and 4.00');
            } else {
                this.setCustomValidity('');
            }
        });
        // Clear custom validity on input so re-typing removes error
        gpaInput.addEventListener('input', function () {
            this.setCustomValidity('');
        });
    }

    // Skills field visual feedback
    const skillsInput = form.querySelector('input[name="skills"]');
    if (skillsInput) {
        skillsInput.addEventListener('input', function () {
            const skills = this.value.split(',').map(s => s.trim()).filter(Boolean);
            this.style.borderColor = skills.length > 0 ? 'var(--kf-primary)' : '';
        });
    }
});
