document.addEventListener('DOMContentLoaded', function() {
    const checkoutForm = document.getElementById('checkoutForm');
    const phoneInput = document.getElementById('phone');

    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            const x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
        });
    }

    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            // Тут може бути додаткова клієнтська валідація,
            // наприклад, перевірка довжини імені або формату email перед відправкою.
            
            // Якщо валідація пройшла успішно, форма відправляється на сервер.
        });
    }
});