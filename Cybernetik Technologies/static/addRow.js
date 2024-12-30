function addNewRow() {
    const tableBody = document.querySelector("#data-table tbody");

    // Create a new row
    const newRow = document.createElement("tr");
    // Add editable cells and an Apply button to the row
    // Replace with the actual column names or dynamically fetch them
const columnNames = ["Date_Time", "Pallet_No", "Total_Bag_Count", "Total_time", "Avg_Bag_time", "Bag_Wait_time"];

// Generate table row dynamically
let rowHTML = `<td></td>`;
columnNames.forEach(() => {
    rowHTML += `<td contenteditable="true"></td>`;
});
rowHTML += `<td><button type="button" onclick="applyChanges(this)">Apply</button></td>`;
newRow.innerHTML = rowHTML;

// Append the new row to the table body
tableBody.appendChild(newRow);

// Scroll to the end of the page
newRow.scrollIntoView({ behavior: "smooth", block: "end" });

}

function applyChanges(button) {
    const newRow = button.closest("tr");

    // Collect the data from all editable cells (excluding the serial number and Apply button)
    const newData = Array.from(newRow.querySelectorAll("td:not(:first-child):not(:last-child)"))
        .map(td => td.textContent.trim());

    console.log("Data to send to backend:", newData); // Log the data to verify it

    // Ensure exactly 6 values are provided
    if (newData.length !== 6) {
        alert("Error: You must provide exactly 6 values.");
        return;
    }

    // Send the data to the backend for insertion
    fetch("/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: newData })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert("Row added successfully!");
            location.reload(); // Reload the page to refresh the table
        } else {
            alert("Error adding row: " + result.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An unexpected error occurred. Please try again.");
    });
}
