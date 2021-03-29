document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".sidenav");
  var instances = M.Sidenav.init(elems, { edge: "right" });
});
document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".dropdown-trigger");
  var instances = M.Dropdown.init(elems, { alignment: "right" });
});

const editBtn = document.querySelectorAll(".editBtn");
for (el of editBtn) {
  let clicked = false;
  el.addEventListener("click", function (e) {
    clicked = !clicked;
    const edit_selected = e.target.getAttribute("data-id");
    const selected_row = document.getElementById(edit_selected);
    const dataType = e.target.getAttribute("data-type");
    if (clicked) {
      selected_row.removeAttribute("disabled");
    } else {
      selected_row.setAttribute("disabled", "");
      const url = `/edit/${edit_selected}`;
      const data = selected_row.value;
      const type = $.ajax({
        type: "POST",
        url: url,
        data: {
          pageType: dataType,
          string: data,
        },
      });
    }
  });
}

const clear_btn = document.querySelectorAll(".clearBtn");
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
    });
  });
}

const daily = JSON.parse(document.getElementById("daily").textContent);
const month = JSON.parse(document.getElementById("month").textContent);
var daily_created_date = new Set();
daily.add_list.forEach((date) => {
  daily_created_date.add(date.created);
});
var month_created_date = new Set();
month.add_list.forEach((date) => {
  month_created_date.add(date.created);
});

const dropdown_container = document.getElementById("daily_dropdown_by_created");
[...daily_created_date].map((li) => {
  const daily_element = document.createElement("li");
  daily_element.setAttribute("class", "daily_dropdown_by_created_element");
  daily_element.textContent = li;
  dropdown_container.append(daily_element);
});

const created_sort_btn = document.querySelectorAll(".sort_by_created");
for (el of created_sort_btn) {
  el.addEventListener("click", function (e) {});
}
