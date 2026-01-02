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

      if (!response.ok) {
        console.error("Backend error:", result);
        alert("Prediction failed on server");
        return;
      }

      const resultBox = document.getElementById("resultBox");
      const resultValue = document.getElementById("resultValue");

      resultValue.innerText = result.efficiency + " %";
      resultBox.classList.remove("d-none");

    } catch (error) {
      console.error("Prediction error:", error);
      alert("Server error. Please try again.");
    }
  });

});
