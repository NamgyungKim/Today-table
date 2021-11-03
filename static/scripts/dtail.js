// $.ajax({
//     type: 'GET',
//     url: '/main',
//     data:{},
//     success: function (response) {
//         alert("ajax success")	//연결을 확인한다
//         let items = JSON.parse('{{ items | tojson | safe}}');
//         console.log(response)
//         console.log(items)
//     }
// })

$(document).ready(function () {
  get_list()
})

function get_list() {
  $.ajax({
    type: 'GET',
    crossDomain: true,
    url: 'http://openapi.foodsafetykorea.go.kr/api/sample/COOKRCP01/json/1/5',
    data: {},
    success: function (response) {
      let dishes = response['COOKRCP01']['row']
      
      console.log(dishes[0])

      let i = 0
      let dishName = dishes[i]['RCP_NM']
      let kind = dishes[i]['RCP_PAT2']
      let url = dishes[i]['ATT_FILE_NO_MAIN']
      let ingredient = dishes[i]['RCP_PARTS_DTLS'] // 재료
      

      console.log(dishName, kind, url, ingredient)

      let temp_html = `<div className="dish">
                        <img src = "${url}" alt = "dish-image"/ >
                        <h3 className = "title">${kind} ${dishName} </h3>
                      </div>`

      $('.dish-lists').append(temp_html)
    },
  })
}
