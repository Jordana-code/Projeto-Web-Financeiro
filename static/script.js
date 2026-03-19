document.getElementById("finance-form").addEventListener("submit", function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch("/resultado", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById("category-analysis");

        container.innerHTML = `
            <img src="/static/${data.grafico}?t=${new Date().getTime()}" class="rounded-xl shadow-lg mb-4">
            <img src="/static/${data.grafico2}?t=${new Date().getTime()}" class="rounded-xl shadow-lg">
        `;
    })
    .catch(error => {
        console.error("Erro:", error);
    });
});