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
    const modal_data_content = e.target
      .closest("div")
      .getAttribute("data-content");

    const list_container = document.getElementById(
      "modal_content_list_contents"
    );
    list_container.innerHTML = "";
    const selected = e.target.closest(".individual_card_wrap");
    const modalContainer = $(".modal_content__header");

    modalContainer.text(modal_data_content);

    const getting_date_list = document.getElementsByClassName(
      "home_list_set_wrap"
    );

    let adding_list_container = document.createElement("div");
    adding_list_container.setAttribute("class", "added_modal_content_div");
    for (var list of getting_date_list) {
      const get_data_content = list.getAttribute("data-content");
      if (get_data_content == modal_data_content) {
        const cln = list.cloneNode(true);
        adding_list_container.append(cln);
      }
    }
    list_container.append(adding_list_container);

    // create modal input and submit button
    // input container
    const modal_input_container = document.createElement("div");
    modal_input_container.className = "modal_input_container";

    const modal_input_value_wrap = document.createElement("div");
    modal_input_value_wrap.className = "modal_input_value";
    const modal_input_value = document.createElement("INPUT");
    modal_input_value.setAttribute("type", "text");
    modal_input_value.setAttribute("name", "todo-by-date");
    modal_input_value.setAttribute("placeholder", "Todo List");
    modal_input_value.setAttribute("data-content", modal_data_content);
    modal_input_value_wrap.appendChild(modal_input_value);
    modal_input_container.appendChild(modal_input_value_wrap);

    // modal submit button
    const modal_submit_button_wrap = document.createElement("div");
    modal_submit_button_wrap.className = "modal_submit_button";
    const modal_submit_button = document.createElement("button");
    modal_submit_button.className = "modal_submit_button_box";
    modal_submit_button.textContent = "Add";
    modal_submit_button_wrap.appendChild(modal_submit_button);
    modal_input_container.appendChild(modal_submit_button_wrap);

    list_container.append(modal_input_container);

    const input_from_modal = document.querySelector(".modal_input_value");
    const input_button_from_modal = document.querySelector(
      ".modal_submit_button"
    );
    input_button_from_modal.addEventListener("click", function () {
      const added_input_from_modal = input_from_modal.firstChild.value;
      const input_date_from_modal = input_from_modal.firstChild.getAttribute(
        "data-content"
      );

      console.log(added_input_from_modal);
      console.log(input_date_from_modal);
    });
  });
}