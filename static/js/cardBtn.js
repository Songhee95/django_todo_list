document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".modal");
  var instances = M.Modal.init(elems, options);
});

// Or with jQuery

$(document).ready(function () {
  $(".modal").modal();
});

const cardBtnElement = $(".individual_card_wrap");
cardBtnElement.click(function (e) {
  const selected = e.target.closest(".individual_card_wrap");
  const selectedDate = selected.getAttribute("data-id");
  const modalContainer = $(".modal_content__header");
  modalContainer.text(selectedDate);
});
