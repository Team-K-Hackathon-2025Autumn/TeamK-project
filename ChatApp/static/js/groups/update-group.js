/*
グループを更新するモーダルの制御
*/

const updateButton = document.getElementById("group-update-button");
const updateChannelModal = document.getElementById("update-group-modal");
const updatePageButtonClose = document.getElementById(
  "update-page-close-button"
);

// モーダルが存在するページのみ（uidとグループidが同じ時のみ）
if (updateGroupModal) {
  // モーダル表示ボタンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateGroupModal.style.display = "flex";
  });

  // モーダル内のXボタンが押された時にモーダルを非表示にする
  updatePageButtonClose.addEventListener("click", () => {
    updateGroupModal.style.display = "none";
  });

  // 画面のどこかが押された時にモーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateGroupModal) {
      updateGroupModal.style.display = "none";
    }
  });
}

// update-group-modalが表示されている時に Ctrl/Command + Enter で送信
function sendUpdateForm() {
  const newGroupName = document.updateGroupForm.groupName.value;

  if (newGroupName !== "") {
    document.updateGroupForm.submit();
  }
}
