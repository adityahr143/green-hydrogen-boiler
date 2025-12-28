document.getElementById("predictForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    const response = await fetch("/predict", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    console.log(result); // debug

    document.getElementById("efficiency").innerText =
        result.efficiency !== undefined
            ? result.efficiency + " %"
            : "Prediction error";
});
