    // For navbar scrolling kapag pinindot yung mga links sa navbar
    document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.navbar-links a').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                if (href === "#home") {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else {
                    const section = document.querySelector(href);
                    if (section) {
                        section.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            }
        });
    });
});

