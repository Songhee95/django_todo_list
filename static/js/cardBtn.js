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
      "home_list_set_wrap_for_modal"
    );

    let adding_list_container = document.createElement("div");
    adding_list_container.setAttribute("class", "added_modal_content_div");
    for (var list of getting_date_list) {
      const get_data_content = list.getAttribute("data-content");
      if (get_data_content == modal_data_content) {
        const cln = list.cloneNode(true);
        const modal_edit_button = cln.querySelectorAll(".editBtn");
        modal_edit_button.forEach((button) => {
          button.classList.add("modal_edit_button");
        });
        const modal_clear_button = cln.querySelectorAll(".home_list_checkbox");
        modal_clear_button.forEach((button) => {
          button.classList.add("modal_clear_button");
        });
        const modal_date_to_remove = cln.querySelectorAll(
          ".home_list_date_column"
        );
        modal_date_to_remove.forEach((element) => {
          element.parentNode.removeChild(element);
        });
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
      if (added_input_from_modal !== "") {
        $.ajax({
          type: "POST",
          url: "/modal_pop",
          data: {
            pageType: "modal",
            string: added_input_from_modal,
            date: input_date_from_modal,
          },
        }).then((res) => location.reload());
      }
    });

    const editBtn = document.querySelectorAll(".modal_edit_button");
    for (el of editBtn) {
      let clicked = false;
      el.addEventListener("click", function (e) {
        clicked = !clicked;
        const edit_selected = e.target.getAttribute("data-id");
        const modal_parent_selected_row = e.target.closest(
          "div.home_list_set_wrap"
        );
        const modal_edit_input = modal_parent_selected_row.querySelector(
          "input.displayed_list"
        );
        const dataType = e.target.getAttribute("data-type");

        if (clicked) {
          modal_edit_input.removeAttribute("disabled");
        } else {
          modal_edit_input.setAttribute("disabled", "");
          const url = `/edit/${edit_selected}`;
          const data = modal_edit_input.value;
          $.ajax({
            type: "POST",
            url: url,
            data: {
              pageType: dataType,
              string: data,
            },
          }).then((res) => location.reload());
        }
      });
    }

    const clear_btn = document.querySelectorAll(".modal_clear_button");
    for (el of clear_btn) {
      el.addEventListener("click", function (e) {
        const checked_el = e.target.getAttribute("data-id");
        const dataType = e.target.getAttribute("data-type");
        const url = `/edit/${checked_el}`;
        if (e.target.checked) {
          status = "True";
        } else {
          status = "False";
        }
        $.ajax({
          type: "POST",
          url: url,
          data: {
            pageType: dataType,
            checked: status,
          },
        }).then((res) => location.reload());
      });
    }
  });
}

const modal_edit_cleared = modal_parent_selected_row.querySelector(
  "input.clearBtn"
);
console.log(modal_edit_cleared);
const checked_el = modal_edit_cleared.getAttribute("data-id");
const dataType_edit_cleared = modal_edit_cleared.getAttribute("data-type");
console.log(checked_el);
console.log(dataType_edit_cleared);
