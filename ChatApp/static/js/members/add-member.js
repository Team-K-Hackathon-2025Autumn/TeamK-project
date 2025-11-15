/*
メンバーを追加するモーダルの制御
*/
window.addEventListener("DOMContentLoaded", () => {
  const reopen = document.body.dataset.reopenModal;
  if (reopen === "add-member") {
    const modal = document.getElementById("add-member-modal");
    if (modal) modal.style.display = "flex";
  }
});

const addButton = document.getElementById("member-add-button");
const addMemberModal = document.getElementById("add-member-modal");
const addPageButtonClose = document.getElementById("add-page-close-button");

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (addMemberModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  addButton.addEventListener("click", () => {
    addMemberModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  addPageButtonClose.addEventListener("click", () => {
    addMemberModal.style.display = "none";
    const flashes = addMemberModal.querySelector(".flashes");
    if (flashes) flashes.remove();
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == addMemberModal) {
      addMemberModal.style.display = "none";
       const flashes = addMemberModal.querySelector(".flashes");
       console.log(flashes);
       
       if (flashes) flashes.remove();
    }
  });
}

// add-member-modalが表示されている時に Ctrl/Command + Enter で送信
function sendAddForm() {
  const email = document.addMemberForm.email.value;

  if (email !== "") {
    document.addMemberForm.submit();
  }
}
