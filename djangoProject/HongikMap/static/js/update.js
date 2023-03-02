// csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function building_preprocessing(e){
    var building=$('#buildingName').val();
    $.ajax({
        url:'building_preprocessing',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'building': building,
        },
        datatype: 'json',
        success: function (data){
            console.log('success');
        }
    });
}

function XtoX_preprocessing(e){
    $.ajax({
        url: 'XtoX_preprocessing',
        type:'POST',
        data:{
            'csrfmiddlewaretoken': csrftoken,
        },
        datatype:'json',
        success:function(data){
            console.log('success');
        }
    });
}

function external_preprocessing(e){

}