$.ajax({
    type: 'GET',
    url: '/main',
    data:{},
    success: function (response) {
        alert("ajax success")	//연결을 확인한다
        console.log(response)
    }
})

    // $(document).ready(function () {
    //     get_list()
    // })
    //
    // function get_list() {
    //     $.ajax({
    //         type: "GET",
    //         url: "http://api.nongsaro.go.kr/service/recomendDiet/recomendDietList?apiKey=20211101HGX1FPG4TTRUPRUQ36Y8MA",
    //         data: {},
    //         success: function (response) {
    //             let rows = response;
    //             console.log(rows)
    //         }
    //     })
    // }