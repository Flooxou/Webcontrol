document.addEventListener("DOMContentLoaded", () => {
    const menuIcon = document.getElementById("menu");
    const navbar = document.querySelector(".navbar");
    const navbarContainer = document.querySelector(".navbar-container");
    const container = document.querySelector(".container");

    menuIcon.addEventListener("click", () => {
        // Toggle the classes to open/close the navbar
        navbar.classList.toggle("navbar-open");
        navbarContainer.classList.toggle("navbar-container-open");
        container.classList.toggle("container-open");

        // Switch the icon
        if (navbar.classList.contains("navbar-open")) {
            menuIcon.classList.remove("fa-bars");
            menuIcon.classList.add("fa-xmark");
        } else {
            menuIcon.classList.remove("fa-xmark");
            menuIcon.classList.add("fa-bars");
        }
    });

    const toggleItems = document.querySelectorAll(".dropbox-toggle");

    toggleItems.forEach(item => {
        item.addEventListener("click", () => {
            const dropbox = item.nextElementSibling; // Le sous-menu associé
            const icon = item.querySelector("i"); // Le chevron

            if (dropbox.style.display === "block") {
                // Ferme le menu
                dropbox.classList.remove("open");
                setTimeout(() => {
                    dropbox.style.display = "none"; // Attend la fin de la transition
                }, 300);
                icon.classList.remove("open");
            } else {
                // Ouvre le menu
                dropbox.style.display = "block";
                setTimeout(() => {
                    dropbox.classList.add("open");
                }, 10);
                icon.classList.add("open");
            }
        });
    });

    initVaultSelection();
});

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('certificateForm');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Empêche le rechargement de la page
        
        // Récupération des données du formulaire
        const formData = new FormData(form);
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            if (data.status === 'success') {
                // Affiche les résultats dans un pop-up
                
                const popupContent = `
                    <div style="margin-bottom: 20px;">
                    <h3>Certificate</h3>
                    <div class="content-box">
                    <pre>${data.certificate}</pre>
                    </div>
                    <button class="btn" onclick="copyToClipboard(\`${data.certificate}\`)">Copy Certificate</button>
                    </div>
                    <div style="margin-bottom: 20px;">
                    <h3>Private Key</h3>
                    <div class="content-box">
                    <pre>${data.private_key}</pre>
                    </div>
                    <button class="btn" onclick="copyToClipboard(\`${data.private_key}\`)">Copy Private Key</button>
                    </div>
                    <div style="margin-bottom: 20px;">
                    <h3>CA Chain</h3>
                    <div class="content-box">
                    <pre>${data.ca_chain}</pre>
                    </div>
                    <button class="btn" onclick="copyToClipboard(\`${data.ca_chain}\`)">Copy CA Chain</button>
                    </div>
                `;
                showPopup(popupContent);
            } else {
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Check the console for details.');
        }
    });

    function showPopup(content) {
        const popup = document.createElement('div');
        popup.style.position = 'fixed';
        popup.style.top = '50%';
        popup.style.left = '50%';
        popup.style.transform = 'translate(-50%, -50%)';
        popup.style.background = '#fff';
        popup.style.padding = '20px';
        popup.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        popup.style.zIndex = '1000';
        popup.style.width = '80%';
        popup.style.maxWidth = '600px';
        popup.style.maxHeight = '80%';
        popup.style.overflowY = 'auto';
        popup.style.borderRadius = '10px';

        popup.innerHTML = `
            <div style="text-align: right;">
                <button onclick="this.parentElement.parentElement.remove()" style="background: red; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Close</button>
            </div>
            ${content}
        `;

        document.body.appendChild(popup);
    }

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    });
}

async function initVaultSelection() {
    const selectElements = document.querySelectorAll('select[name="vault_id"]');
    if (!selectElements.length) return;

    try {
        const res = await fetch('http://localhost:5000/vault/servers');
        const servers = await res.json();
        selectElements.forEach(sel => {
            sel.innerHTML = servers.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        });

        const activeRes = await fetch('http://localhost:5000/vault/servers/active');
        const active = await activeRes.json();
        if (active && active.id) {
            selectElements.forEach(sel => { sel.value = active.id; });
            const activeSpan = document.getElementById('active-vault-name');
            if (activeSpan) {
                activeSpan.textContent = `${active.name} (${active.address})`;
            }
        }
    } catch (e) {
        console.error('Failed to load servers', e);
    }
}

});
