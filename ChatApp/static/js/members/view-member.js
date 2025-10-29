/*
メンバー一覧を表示するモーダルの制御
*/

const viewButton = document.getElementById("member-view-button");
const viewMemberModal = document.getElementById("view-member-modal");
const viewPageButtonClose = document.getElementById("view-page-close-button");

// モーダル表示ボタンが押された時にモーダルを表示する
viewButton.addEventListener("click", () => {
  viewMemberModal.style.display = "flex";
});

// モーダル内のXボタンが押された時にモーダルを非表示にする
viewPageButtonClose.addEventListener("click", () => {
  viewMemberModal.style.display = "none";
});

// 画面のどこかが押された時にモーダルを非表示にする
addEventListener("click", (e) => {
  if (e.target == viewMemeberModal) {
    viewMemberModal.style.display = "none";
  }
});
