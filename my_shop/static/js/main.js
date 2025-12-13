document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.add-to-cart-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const btn = this.querySelector('button');
            const originalText = btn.innerText;
            
            btn.innerText = '✓ Добавлено';
            btn.style.backgroundColor = '#00b894';
            
            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.backgroundColor = '';
            }, 2000);
        });
    });


    const alerts = document.querySelectorAll('.alert');
    if(alerts) {
        setTimeout(() => {
            alerts.forEach(el => el.style.opacity = '0');
        }, 3000);
    }
});