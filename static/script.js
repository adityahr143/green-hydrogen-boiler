document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("predictForm");

  if (!form) {
    console.error("Predict form not found");
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
      const response = await fetch("/predict", {
        method: "POST",
        body: formData
      });

      const result = await response.json();

      const resultBox = document.getElementById("resultBox");
      const resultValue = document.getElementById("resultValue");

      if (result.efficiency !== undefined) {
        resultValue.innerText = result.efficiency + " %";
        resultBox.classList.remove("d-none");
      } else {
        alert("Prediction failed. Check inputs.");
      }

    } catch (error) {
      console.error("Prediction error:", error);
      alert("Server error. Please try again.");
    }
  });

});
