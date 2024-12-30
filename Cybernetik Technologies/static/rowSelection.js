function attachRowClickListeners() {
    const tableRows = document.querySelectorAll("#data-table tbody tr");

    tableRows.forEach(row => {
        row.addEventListener("click", () => {
            tableRows.forEach(r => r.classList.remove("selected"));
            row.classList.add("selected");
        });
    });
}

// Call this function after the table is re-rendered
document.addEventListener('DOMContentLoaded', attachRowClickListeners);
