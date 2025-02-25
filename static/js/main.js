function toggleFilters() {
    const searchInput = document.getElementById('searchInput');
    const filtersPanel = document.getElementById('filtersPanel');
    searchInput.classList.toggle('hide');
    filtersPanel.classList.toggle('show');
}
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const dairyTypeSelect = document.getElementById('dairyTypeSelect');
    const courseTypeSelect = document.getElementById('courseTypeSelect');

    function submitForm() {
        searchForm.submit();
    }

    dairyTypeSelect.addEventListener('change', submitForm);
    courseTypeSelect.addEventListener('change', submitForm);

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        submitForm();
    });
});

function togglePassword(icon) {
    const passwordInput = icon.previousElementSibling;
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

function toggleUserDropdown() {
    const dropdownContent = document.getElementById('userDropdownContent');
    dropdownContent.classList.toggle('show');
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
