function toggle_like(food_num, type) {
  let $a_like = $(`#${food_num} a[aria-label='heart']`);
  let $i_like = $a_like.find("i");
  if ($i_like.hasClass("fa-heart")) {
    $.ajax({
      type: "POST",
      url: "/update_like",
      data: {
        food_num_give: food_num,
        type_give: type,
        action_give: "unlike",
      },
      success: function (response) {
        $i_like.addClass("fa-heart-o").removeClass("fa-heart");
        $a_like.find("span.like-num").text(response["count"]);
      },
    });
  } else {
    $.ajax({
      type: "POST",
      url: "/update_like",
      data: {
        food_num_give: food_num,
        type_give: type,
        action_give: "like",
      },
      success: function (response) {
        $i_like.addClass("fa-heart").removeClass("fa-heart-o");
        $a_like.find("span.like-num").text(response["count"]);
      },
    });
  }
}
function userpage() {
  window.location.href = "/user/{{ user_info.username }}";
}

function show_modal() {
  $(".modal").addClass("show");
}

function hide_modal() {
  $(".modal").removeClass("show");
}
