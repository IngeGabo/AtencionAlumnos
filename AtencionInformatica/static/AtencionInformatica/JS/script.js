/*Para la barra de navegacion*/

function loadContent(page) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', page + '.html', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('content').innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}

// Cargar contenido inicial (por ejemplo, la página de inicio)
window.onload = function() {
    loadContent('inicio');
};

/*Para trayectorias*/
function initModalListeners() {
    document.querySelectorAll('[id^="openModalBtn"]').forEach(button => {
        const modalId = button.id.replace('openModalBtn', 'modal_container');
        const modal_container = document.getElementById(modalId);

        if (modal_container) {
            button.addEventListener('click', () => {
                modal_container.classList.add("show");
                console.log(`Botón ${button.id} presionado`);
            });

            const closeModalBtn = modal_container.querySelector('[id^="closeModalBtn"]');
            if (closeModalBtn) {
                closeModalBtn.addEventListener('click', () => {
                    modal_container.classList.remove('show');
                    console.log(`Modal ${modalId} cerrado`);
                });
            }

            modal_container.addEventListener('click', (event) => {
                if (event.target === modal_container) {
                    modal_container.classList.remove('show');
                    console.log(`Modal ${modalId} cerrado por clic externo`);
                }
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initModalListeners();

    const content = document.getElementById('content');
    const observer = new MutationObserver(() => {
        initModalListeners();
    });

    observer.observe(content, { childList: true, subtree: true });
});




