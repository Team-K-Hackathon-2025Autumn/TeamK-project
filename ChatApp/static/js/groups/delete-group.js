export const initDeletegroupModal = () => {
  const deletePageButtonClose = document.getElementById(
    "delete-page-close-button"
  );

  const deletegroupModal = document.getElementById("delete-group-modal");

  deletePageButtonClose.addEventListener("click", () => {
    deletegroupModal.style.display = "none";
  });

  addEventListener("click", (e) => {
    if (e.target == deletegroupModal) {
      deletegroupModal.style.display = "none";
    }
  });
};