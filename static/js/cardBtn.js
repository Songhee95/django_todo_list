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
    const list_container = document.getElementById(
      "modal_content_list_contents"
    );
    list_container.innerHTML = "";
    const selected = e.target.closest(".individual_card_wrap");
    const selectedDate = selected.getAttribute("data-id");
    const modalContainer = $(".modal_content__header");

    modalContainer.text(selectedDate);

    const getting_date_list = document.getElementsByClassName(
      "home_list_set_wrap"
    );

    let adding_list_container = document.createElement("div");
    adding_list_container.setAttribute("class", "added_modal_content_div");
    for (var list of getting_date_list) {
      const get_data_content = list.getAttribute("data-content");
      if (get_data_content == selectedDate) {
        const cln = list.cloneNode(true);
        adding_list_container.append(cln);
      }
    }
    list_container.append(adding_list_container);
    // ajax call
    // $.ajax({
    //   type: "POST",
    //   url: "/modal_pop",
    //   data: {
    //     selected: selectedDate,
    //   },
    // });
  });
}
