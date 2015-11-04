function select_change() {
        $.ajax({
        url: "gettest/",
        data: {"id": document.getElementById('q_sel').value },
        type: "GET",
        dataType: "json",
        success: function( resp ) {
            document.getElementById('ec').innerHTML = '&nbsp;';
            $('#btn1').prop("disabled", false)
            $.each( resp, function( key, value ) {
            console.log( key + " : " + value );
            if (key == 'qc'){
              qc = value
              }
            if (key != 'ec'){
              document.getElementById(key).innerHTML = value;
              }
            else{
              if (value < qc){
                document.getElementById(key).innerHTML = 'В БД недостаточно вопросов для данного теста';
                $('#btn1').attr("disabled", "disabled")
                }
              }
            });
        },
        error: function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        },
        complete: function( xhr, status ) {
            console.log( "The request is complete!" );
        }
    });
}
$().ready(function(){
    select_change();
})
