const inputSubmit = document.getElementById('input-submit');
inputSubmit.addEventListener('click', async function (event) {
  event.preventDefault();
  inputSubmit.disabled = true;
  isModalCloseDisabled = true;

  let dotNum = 0;
  let inputSubmitButtonBaseText = 'AIにリクエスト中';
  inputSubmit.innerText = inputSubmitButtonBaseText;
  setInterval(() => {
    dotNum = (dotNum % 3) + 1;
    inputSubmit.innerText = inputSubmitButtonBaseText + '.'.repeat(dotNum);
  }, 1000);

  const form = document.getElementById('ingredient-form');
  const formData = new FormData(form);
  const ingredientNames = formData.getAll('name');
  const ingredientQuantities = formData.getAll('quantity');
  const ingredientUnits = formData.getAll('unit');
  const ingredients = [];
  for (let i = 0; i < ingredientNames.length; i++) {
    ingredients.push({
      name: ingredientNames[i],
      quantity: ingredientQuantities[i],
      unit: ingredientUnits[i],
    });
  }

  const request = formData.get('request');
  const menuCandidateCount = formData.get('menuCandidateCount');

  const request_data = {
    ingredients: ingredients,
    request: request,
    menuCandidateCount: menuCandidateCount,
  };

  try {
    const response = await fetch(`/group/${group.id}/menu`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request_data),
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data);
      window.location.href = data.redirect_url;
    }
  } catch (error) {
    console.error('Error:', error);
  }
});
