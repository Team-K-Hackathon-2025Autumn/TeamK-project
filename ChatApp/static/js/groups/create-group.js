export const initCreategroupModal = () => {
  const creategroupModal = document.getElementById("create-group-modal"); 
  const addPageButtonClose = document.getElementById("add-page-close-button"); 
  const creategroupButton = document.getElementById("create-group-button"); /// pagination.jsが設定するボタン

  creategroupButton.addEventListener("click", () => {
    creategroupModal.style.display = "flex"; 
  });

  addPageButtonClose.addEventListener("click", () => {

    creategroupModal.style.display = "none"; 
  });

  addEventListener("click", (e) => {
    if (e.target == creategroupModal) {
      creategroupModal.style.display = "none"; 
    }
  });

  document.addEventListener("keydown", (e) => {
   const form = document.creategroupForm;
   const newgroupName = form.groupName.value.trim();
   const modal = document.getElementById("create-group-modal");

   const isModalVisible = getComputedStyle(modal).display !== "none";

   if (e.code === "Enter") e.preventDefault();

   const ctrlOrCmd = e.ctrlKey || e.metaKey;

   if (ctrlOrCmd && e.code === "Enter" && isModalVisible && newgroupName) {
    form.submit();
   }
  });

};
