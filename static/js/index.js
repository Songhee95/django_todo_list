document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".sidenav");
  var instances = M.Sidenav.init(elems, { edge: "right" });
});

const editBtn = document.querySelectorAll(".editBtn");
for (el of editBtn) {
  let clicked = false;
  el.addEventListener("click", function (e) {
    clicked = !clicked;
    const edit_selected = e.target.getAttribute("data-id");
    const selected_row = document.getElementById(edit_selected);
    if (clicked) {
      selected_row.removeAttribute("disabled");
    } else {
      selected_row.setAttribute("disabled", "");
      const url = `/edit/${edit_selected}`;
      const data = selected_row.value;
      $.ajax({
        type: "POST",
        url: url,
        data: {
          string: data,
        },
      });
    }
  });
}
