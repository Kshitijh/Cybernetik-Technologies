function editRow() {
    const selectedRow = document.querySelector("#data-table tbody tr.selected");
    if (!selectedRow) {
        alert("Please select a row to edit.");
        return;
    }

    // Get the unique Date and Time identifier
    const uniqueIdentifier = selectedRow.getAttribute("data-index");

    // Collect the data from the editable cells (excluding the serial number)
    const updatedData = Array.from(selectedRow.querySelectorAll("td:not(:first-child)"))
        .map(td => td.textContent.trim());

    // Send the updated data to the server to be updated in the database
    fetch(`/edit/${encodeURIComponent(uniqueIdentifier)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: updatedData })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert("Row updated successfully!");
            location.reload(); // Reload the page to refresh the table
        } else {
            alert("Error updating row: " + result.error);
        }
    });
}
