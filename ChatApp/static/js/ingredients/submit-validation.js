document.addEventListener('DOMContentLoaded', () => {
  const submitButton = document.getElementById('input-submit');
  const form = document.getElementById('ingredient-form');
  const addInputArea = document.getElementById('add-input-area');

  function validateForm() {
    let allRowsValid = true;
    const rows = addInputArea.querySelectorAll('.input-area');
    if (rows.length == 0) {
      allRowsValid = false;
    } else {
      for (const row of rows) {
        const nameInput = row.querySelector('input[name="name"]').value.trim();

        const quantityInput = row
          .querySelector('input[name="quantity"]')
          .value.trim();

        const unitInput = row.querySelector('select[name="unit"]').value.trim();

        if (nameInput == '' || quantityInput == '' || unitInput == '""') {
          allRowsValid = false;
          break;
        }
      }
    }
    // submitButton.disabled = !allRowsValid;
    // if (!submitButton.disabled) {
    //   submitButton.style.backgroundColor = '#D87C58';
    // } else {
    //   submitButton.style.backgroundColor = '#808080';
    // }
  }

  form.addEventListener('input', validateForm);
  addInputArea.addEventListener('click', validateForm);

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === 'childList') {
        validateForm();
      }
    }
  });

  observer.observe(addInputArea, {
    childList: true,
  });

  validateForm();
});
