// $.ajax({
//     type: 'GET',
//     url: '/main',
//     data:{},
//     success: function (response) {
//         alert("ajax success")	//연결을 확인한다
//         let items = JSON.parse('{{ items | tojson | safe}}');
//         // console.log(response)
//         console.log(items)
//     }
// })

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
  window.location.href="/user/{{ user_info.username }}";
}

function sign_out() {
  $.removeCookie("mytoken", { path: "/" });
  alert("정상적으로 로그아웃 되었습니다.");
  window.location.href = "/";
}
function nav_show() {
  if ($(".nav").css("display") == "none") {
    $(".nav").show();
    $(".nav").addClass("show");
  } else {
    $(".nav").hide();
    $(".nav").removeClass("show");
  }
}

function show_modal() {
  $(".modal").removeClass("hidden");
}

function hide_modal() {
  $(".modal").addClass("hidden");
}

$(document).ready(function () {
  // get_list();
});

// 프로필클릭시 로그아웃버튼 show
$(".user").click(function () {
  if ($(".nav").hasClass("show")) {
    $(".nav").removeClass("show");
  } else {
    $(".nav").addClass("show");
  }
});
//top버튼 클릭시 위로스크롤
$("#top-btn").click(function () {
  $("html, body").animate({ scrollTop: 0 }, 400);
  return false;
});
//top버튼 스트롤200부터 보임
$(window).scroll(function () {
  if ($(this).scrollTop() > 200) {
    $("#top-btn").fadeIn();
  } else {
    $("#top-btn").fadeOut();
  }
});

function get_list() {
  $.ajax({
    type: "GET",
    crossDomain: true,
    url: "http://openapi.foodsafetykorea.go.kr/api/sample/COOKRCP01/json/1/5",
    data: {},
    success: function (response) {
      let dishes = response["COOKRCP01"]["row"];

      dishes.forEach((dish, idx) => {
        let dishName = dish["RCP_NM"];
        let kind = dish["RCP_PAT2"];
        let url = dish["ATT_FILE_NO_MAIN"];

        console.log(dishName, kind, url);
        if (idx < 3) {
          let temp_html_rc = `<img src="${url}" alt="dish-image"/>`;
          $(".image-container").append(temp_html_rc);
        }

        let temp_html = `<div class="dish">
                                    <img src="${url}" alt="dish-image"/>
                                    <h3 class="title">${kind} ${dishName} </h3>
                                </div>`;

        $(".dish-lists").append(temp_html);
      });
    },
  });
}

// const retryBtn = document.querySelector(".retry-btn");

// console.log(retryBtn);
// function retryQuestion() {
//   console.log("이건 나옴?");

//   // clearQnA();
//   modalContents.innerHTML = "";

//   let temp_html = `
// <h1>질문에 답해주세요.</h1>
//     <div class="question-wrap">
//       <div class="questions-container">
//         <h3 class="question">질문. 밥드실래요? 디저트드실래요?</h3>
//         <label class="box-radio-input"
//           ><input
//             type="radio"
//             name="item_type"
//             value="밥"
//             checked="checked"
//           /><span>밥</span></label
//         >
//         <label class="box-radio-input"
//           ><input type="radio" name="item_type" value="후식" /><span
//             >후식</span
//           ></label
//         >
//       </div>
//       <div class="questions-container">
//         <h3 class="question">질문. 끓이기? 굽기?</h3>
//         <label class="box-radio-input"
//           ><input
//             type="radio"
//             name="item_howto"
//             value="끓이기"
//             checked="checked"
//           /><span>끓이기</span></label
//         >
//         <label class="box-radio-input"
//           ><input type="radio" name="item_howto" value="굽기" /><span
//             >굽기</span
//           ></label
//         >
//       </div>
//       <div class="questions-container">
//         <h3 class="question">질문. 다이어트식? 보양식?</h3>
//         <label class="box-radio-input"
//           ><input
//             type="radio"
//             name="item_cal"
//             value="다이어트식"
//             checked="checked"
//           /><span>다이어트식</span></label
//         >
//         <label class="box-radio-input"
//           ><input type="radio" name="item_cal" value="보양식" /><span
//             >보양식</span
//           ></label
//         >
//       </div>
//     </div>
//     <div class="control-container">
//       <button class="prev" id="prev" disabled>prev</button>
//       <button class="next" id="next">next</button>
//       <button class="submit hide" id="submit">submit</button>
//     </div>
//     <button class="exit-btn" onclick="hide_modal()">X</button>
// `;

//   $(".modal-contents").append(temp_html);

//   // retryBtn.addEventListener("click", (e) => {
//   // });
// }

//// 추천 요리 크기변경
//// 중간 라인 삭제
//// input form 색 디테일에 있는 댓글 폼과 변경
//// 요리 이름 한줄 처리
//// 미디어 쿼리 적용
//// 로고 url 홈페이지로 이동
//// 요리 description 불투명 처리
// 모달
// tab키 포커스 확인

// 검색 기능
