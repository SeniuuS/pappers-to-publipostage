const input = document.getElementById("postalCode");
const list = document.getElementById("autocomplete-list");
const countryCode = document.getElementById("countryCode");

input.addEventListener("input", async () => {
    const query = input.value.trim();
    if (query.length === 0) {
        list.innerHTML = "";
        return;
    }

    const response = await fetch(`/autocompletePostalCode?countryCode=${countryCode.value}&q=${encodeURIComponent(query)}`);
    const results = await response.json();

    list.innerHTML = ""; // Clear previous results
    results.forEach(item => {
        const div = document.createElement("div");
        div.className = "autocomplete-item";
        div.textContent = item.name;
        div.addEventListener("click", () => {
            input.value = item.id;
            list.innerHTML = ""; // Clear the list
        });
        list.appendChild(div);
    });
});

document.addEventListener("click", (event) => {
    if (!list.contains(event.target) && event.target !== input) {
        list.innerHTML = ""; // Hide the list when clicking outside
    }
});