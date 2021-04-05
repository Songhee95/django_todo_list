document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".modal");
  var instances = M.Modal.init(elems);
});

// Or with jQuery

$(document).ready(function () {
  $(".modal").modal();
});

const cardBtnElement = document.querySelectorAll(".individual_card_wrap");
for (el of cardBtnElement) {
  el.addEventListener("click", function (e) {
    const selected = e.target.closest(".individual_card_wrap");
    const selectedDate = selected.getAttribute("data-id");
    const modalContainer = $(".modal_content__header");
    modalContainer.text(selectedDate);

    // ajax call
    $.ajax({
      type: "POST",
      url: "/modal",
      data: {
        selected: selectedDate,
      },
    });
  });
}
