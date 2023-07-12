document.addEventListener("DOMContentLoaded", function() {
  var selectCategoriesBtn = document.getElementById("select-categories-btn");
  var categorySelect = document.getElementById("category-select");

  selectCategoriesBtn.addEventListener("click", function() {
    if (categorySelect.style.display === "none") {
      categorySelect.style.display = "block";
    } else {
      categorySelect.style.display = "none";
    }
  });
});
