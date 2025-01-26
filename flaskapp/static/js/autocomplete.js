document.addEventListener("DOMContentLoaded", function() {
    var searchInput = document.getElementById("search");
    var autocompleteList = document.getElementById("autocomplete-list");

    searchInput.addEventListener("input", function() {
        var query = this.value;
        if (!query) {
            autocompleteList.innerHTML = "";
            return false;
        }

        fetch(`/autocomplete?q=${query}`)
            .then(response => response.json())
            .then(data => {
                autocompleteList.innerHTML = "";
                data.forEach(item => {
                    var div = document.createElement("div");
                    div.innerHTML = item;
                    div.addEventListener("click", function() {
                        searchInput.value = item;
                        autocompleteList.innerHTML = "";
                    });
                    autocompleteList.appendChild(div);
                });
            });
    });

    document.addEventListener("click", function(e) {
        if (e.target !== searchInput) {
            autocompleteList.innerHTML = "";
        }
    });
});