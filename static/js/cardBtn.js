const cardBtnElement = $(".individual_card_wrap");
cardBtnElement.click(function (e) {
  const selected = e.target.closest(".individual_card_wrap");
  const selectedData = selected.getAttribute("data-id");
});
