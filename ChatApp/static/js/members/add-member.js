/*
メンバーを追加するモーダルの制御
*/

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
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == addMemberModal) {
      addMemberModal.style.display = "none";
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
