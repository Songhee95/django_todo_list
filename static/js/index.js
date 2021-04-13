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
    const selected_row = document.getElementsByClassName(edit_selected);
    const dataType = e.target.getAttribute("data-type");
    for (var list of selected_row) {
      if (clicked) {
        list.removeAttribute("disabled");
      } else {
        list.setAttribute("disabled", "");
        const url = `/edit/${edit_selected}`;
        const data = list.value;
        const type = $.ajax({
          type: "POST",
          url: url,
          data: {
            pageType: dataType,
            string: data,
          },
        }).then((res) => location.reload());
      }
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
    }).then((res) => location.reload());
  });
}

const daily = JSON.parse(document.getElementById("daily").textContent);
const month = JSON.parse(document.getElementById("month").textContent);
const return_date_without_duplicate = function (data, createdSet) {
  data.add_list.forEach((date) => {
    createdSet.add(date.created);
  });
};
var daily_created_date = new Set();
return_date_without_duplicate(daily, daily_created_date);

var month_created_date = new Set();
return_date_without_duplicate(month, month_created_date);

const generate_dropdown_date_list = function (
  createdSetList,
  input,
  container
) {
  createdSetList.map((li) => {
    const element = document.createElement("li");
    const className = `${input}_dropdown_lists_by_created`;
    element.setAttribute("class", className);
    element.textContent = li;
    container.append(element);
  });
};
const dropdown_container = document.getElementById("daily_dropdown_by_created");
generate_dropdown_date_list(
  [...daily_created_date],
  "daily",
  dropdown_container
);

const monthly_dropdown_container = document.getElementById(
  "monthly_dropdown_by_created"
);
generate_dropdown_date_list(
  [...month_created_date],
  "month",
  monthly_dropdown_container
);

const display_sorted_data_on_table = function (
  dropdown_list,
  remove_content,
  original_data,
  table
) {
  for (el of dropdown_list) {
    el.addEventListener("click", function (e) {
      const selected_date = e.target.textContent;
      document.getElementById(remove_content).remove();
      const tbody = document.createElement("tbody");
      tbody.setAttribute("id", remove_content);
      original_data.add_list.map((row) => {
        if (row.created === selected_date) {
          const tr_row = document.createElement("tr");

          const td_created = document.createElement("td");
          const p_created = document.createElement("p");
          p_created.textContent = row.created;
          td_created.append(p_created);
          tr_row.append(td_created);

          const td_li = document.createElement("td");
          const p_li = document.createElement("p");
          p_li.textContent = row.li;
          td_li.append(p_li);
          tr_row.append(td_li);

          const td_completed = document.createElement("td");
          const p_label = document.createElement("label");
          const p_completed = document.createElement("input");
          p_completed.setAttribute("type", "checkbox");
          p_completed.setAttribute(row.cleared, "");
          p_completed.setAttribute("disabled", "");
          const p_span = document.createElement("span");
          p_label.append(p_completed);
          p_label.append(p_span);
          td_completed.append(p_label);
          tr_row.append(td_completed);

          const td_updated = document.createElement("td");
          const p_updated = document.createElement("p");
          p_updated.textContent = row.updated;
          td_updated.append(p_updated);
          tr_row.append(td_updated);

          tbody.append(tr_row);
        }
        table.append(tbody);
      });
    });
  }
};
const daily_created_sort_btn = document.querySelectorAll(
  ".daily_dropdown_lists_by_created"
);
const monthly_created_sort_btn = document.querySelectorAll(
  ".month_dropdown_lists_by_created"
);
const daily_history_data_table = document.getElementById(
  "daily_history_data_table"
);
const monthly_history_data_table = document.getElementById(
  "monthly_history_data_table"
);
display_sorted_data_on_table(
  daily_created_sort_btn,
  "daily_history_data_row",
  daily,
  daily_history_data_table
);
display_sorted_data_on_table(
  monthly_created_sort_btn,
  "monthly_history_data_row",
  month,
  monthly_history_data_table
);
