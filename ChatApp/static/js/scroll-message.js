const element = document.getElementById('message-area');
const deleteButton = document.getElementById('button');
const path = window.location.pathname;

const savedscrollTopPosition = sessionStorage.getItem('scrollY_' + path);
if (savedscrollTopPosition) {
  element.scrollTop = savedscrollTopPosition;
} else {
  element.scrollTo(0, element.scrollHeight);
}

sessionStorage.removeItem('scrollY_' + path);

const reactionButtons = document.querySelectorAll('.reaction-message-button');
const deleteButtons = document.querySelectorAll('.delete-message-button');

const buttons = [reactionButtons, deleteButtons];

for (button of buttons) {
  button.forEach((button) => {
    button.addEventListener('click', function (event) {
      const path = window.location.pathname;
      const scrollTopPosition = element.scrollTop;
      sessionStorage.setItem('scrollY_' + path, scrollTopPosition);
    });
  });
}
