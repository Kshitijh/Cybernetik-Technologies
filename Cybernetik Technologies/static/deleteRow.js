function deleteRow() {
    const selectedRow = document.querySelector("#data-table tbody tr.selected");
    if (!selectedRow) {
        alert("Please select a row to delete.");
        return;
    }

    // Get the unique Date and Time identifier
    const uniqueIdentifier = selectedRow.getAttribute("data-index");

    if (confirm(`Are you sure you want to delete the row with Date, Time: ${uniqueIdentifier}?`)) {
        fetch(`/delete/${encodeURIComponent(uniqueIdentifier)}`, {
            method: "DELETE"
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                alert("Row deleted successfully!");
                location.reload(); // Reload the page to refresh the table
            } else {
                alert("Error deleting row: " + result.error);
            }
        });
    }
}
