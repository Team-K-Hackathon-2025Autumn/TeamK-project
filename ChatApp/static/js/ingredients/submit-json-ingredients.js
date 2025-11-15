document
  .getElementById("input-submit")
  .addEventListener("click", function (event) {
    event.preventDefault();
    const form = document.getElementById("ingredient-form");
    const formData = new FormData(form);

    const ingredientNames = formData.getAll("name");
    const ingredientQuantities = formData.getAll("quantity");
    const ingredientUnits = formData.getAll("unit");

    const ingredients = [];
    for (let i = 0; i < ingredientNames.length; i++) {
      ingredients.push({
        name: ingredientNames[i],
        quantity: ingredientQuantities[i],
        unit: ingredientUnits[i],
      });
    }

    const request = formData.get("request");
    const menuCandidateCount = formData.get("menuCandidateCount");

    const request_data = {
      ingredients: ingredients,
      request: request,
      menuCandidateCount: menuCandidateCount,
    };

    fetch(`/group/${group.id}/menu`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request_data),
    })
      .then((response) => {
        if (!response.ok) {
          console.error("エラー"),
            response.status,
            response.status.toExponential();
          return response.text().then((text) => {
            throw new Error(text);
          });
        }
        return response.json();
      })
      .then((result) => {
        console.log("成功:", result);
      })
      .catch((error) => {
        console.error("エラー:", error);
      });
  });
