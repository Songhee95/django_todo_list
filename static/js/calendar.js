$(document).ready(function () {
  obj = {
    January: 1,
    February: 2,
    March: 3,
    April: 4,
    May: 5,
    June: 6,
    July: 7,
    August: 8,
    September: 9,
    October: 10,
    November: 11,
    December: 12,
  };
  const d = new Date();
  const year = d.getFullYear();

  $(".month_next").click(function (e) {
    let displaying_month = $(".displaying_month").text();
    //   send current month +1
    let next = obj[displaying_month] + 1;
    const url = `/calendar/${year}/${next}`;
    window.location.replace(url);

    // $.ajax({
    //   type: "GET",
    //   url: url,
    // }).then((res) => location.reload());
  });

  $(".month_prev").click(function (e) {
    let displaying_month = $(".displaying_month").text();
    //   send current month -1
    let prev = obj[displaying_month] - 1;
    $.ajax({
      type: "POST",
      url: "/calendar",
      data: {
        idx: prev,
      },
    });
  });
});
