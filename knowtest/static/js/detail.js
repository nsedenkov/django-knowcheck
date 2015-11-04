        function set_btn_status(){
            var i = 0;
            var cid = '';
            $('#b_prv').removeAttr("disabled");
            $('#b_nxt').removeAttr("disabled");
            $('#b_ans').removeAttr("disabled");
            if (Data.cur_q == 0){
                $('#b_prv').attr("disabled", "disabled");
            };
            if (Data.cur_q == Data.Qstns.length-1){
                $('#b_nxt').attr("disabled", "disabled");
            };
            if (Data.CurQAnswers.length > 0){
                $('#b_ans').attr("disabled", "disabled");
                for (i=0; i<=Data.CurQChoices.length-1; i++){
                    cid = "c" + i;
                    $('#'+cid).attr("disabled", "disabled");
                };
            };
        }
        function fix_answer(){
            var i = 0;
            var y = 0;
            var cid = '';
            for (i=0; i<=Data.CurQChoices.length-1; i++){
                cid = "c" + i;
                if ($('#'+cid).prop("checked")){
                    Data.CurQAnswers[y] = $('#'+cid).attr("value");
                    y++;
                };
            };
            if (Data.CurQAnswers.length>0){
                var data = "[";
                for (i=0; i<=Data.CurQAnswers.length-1; i++){
                    cid = "c" + i;
                    data = data + "{\"" + cid + "\":\"" + Data.CurQAnswers[i] + "\"}"
                    if (i<Data.CurQAnswers.length-1){
                        data = data + ",";
                    };
                };
                data = data + "]";
                console.log("Serialized data: " + data);
                $.ajax({
                    url: "/knowtest/fixanswer/",
                    data: {"t_id": Data.Initvalue, "q_id": Data.Qstns[Data.cur_q], "c_id": data },
                    type: "GET",
                    dataType: "json",
                    success: function( resp ) {
                        if (resp['q_elps'] > 0){
                            document.getElementById('elpq').innerHTML = "Осталось " + resp['q_elps'] + " вопросов";
                            set_btn_status();
                        }
                        else{
                            clearInterval(c_time);
                            finish_test();
                        }
                    },
                    error: function( xhr, status, errorThrown ) {
                        console.log( "Error: " + errorThrown );
                        console.log( "Status: " + status );
                        console.dir( xhr );
                    },
                    complete: function( xhr, status ) {
                        console.log( "The request is complete!" );
                    }
                });
            }
            else{
                console.log("Array CurQAnswers is empty!");
            };
        }
        function make_question_view(){
            var prefix = '';
            var i = 0;
            var cid = '';
            $.ajax({
                url: "/knowtest/getsubdetail/",
                data: {"t_id": Data.Initvalue, "q_id": Data.Qstns[Data.cur_q] },
                type: "GET",
                dataType: "json",
                success: function( resp ) {
                    // Обнулить массив ответов
                    Data.CurQChoices.length = 0;
                    Data.CurQAnswers.length = 0;
                    $('#sctn2').empty();
                    prefix = "<input type=\"radio\" id=\"";
                    comment = "Выберите ОДИН верный вариант ответа";
                    if (resp['multi']){
                        prefix = "<input type=\"checkbox\" id=\"";
                        comment = "Укажите ВСЕ верные варианты ответа";
                    }
                    $('#q_txt').html(resp['q_txt']);
                    $('#q_typ').html(comment);
                    $.each( resp['answers'], function(key, value){
                        Data.CurQAnswers[key] = value;
                        console.log('CurQAnswers['+key+'] = '+value);
                    });
                    i = 0
                    $.each( resp['choices'], function (key, value){
                        Data.CurQChoices[i] = key;
                        console.log("CurQChoices["+i+"]="+Data.CurQChoices[i]);
                        cid = "c" + i;
                        console.log(cid + " " + value);
                        $('#sctn2').append(prefix + cid + "\" name=\"choice\" value=\""+Data.CurQChoices[i]+"\" />");
                        $('#sctn2').append("<label for=\""+cid+"\">"+value+"</label><br />");
                        console.log('key = '+key+'; Data.CurQAnswers.indexOf='+Data.CurQAnswers.indexOf(Number(key)));
                        if (Data.CurQAnswers.indexOf(Number(key))>-1){
                            $('#'+cid).attr("checked", "checked");
                        };
                        i++;
                    });
                },
                error: function( xhr, status, errorThrown ) {
                    console.log( "Error: " + errorThrown );
                    console.log( "Status: " + status );
                    console.dir( xhr );
                },
                complete: function( xhr, status ) {
                    console.log( "The request is complete!" );
                    set_btn_status();
                }
            });
        }
        function read_questions(){
            $.ajax({
                url: "/knowtest/getdetail/",
                data: {"t_id": Data.Initvalue },
                type: "GET",
                dataType: "json",
                success: function( resp ) {
                    var i = 0
                    $.each( resp, function( key, value ) {
                        console.log( key + " : " + value );
                        Data.Qstns[i] = value;
                        i++;
                    });
                    document.getElementById('elpq').innerHTML = "Тест содержит " + Data.Qstns.length + " вопросов";
                    make_question_view();
                },
                error: function( xhr, status, errorThrown ) {
                    console.log( "Error: " + errorThrown );
                    console.log( "Status: " + status );
                    console.dir( xhr );
                },
                complete: function( xhr, status ) {
                    console.log( "The request is complete!" );
                }
            });
        }
        function show_time(){
            $.ajax({
                url: "/knowtest/gettime/",
                data: {"t_id": Data.Initvalue},
                type: "GET",
                dataType: "json",
                success: function( resp ) {
                    document.getElementById('curtm').innerHTML = resp['ctm'];
                    if (resp['etm'] == 0){
                        // если время вышло - остановить show_time
                        // и завершить тест
                        clearInterval(c_time);
                        finish_test();
                    }
                    else{
                        document.getElementById('elptm').innerHTML = resp['etm'];
                    };
                },
                error: function( xhr, status, errorThrown ) {
                    console.log( "Error: " + errorThrown );
                    console.log( "Status: " + status );
                    console.dir( xhr );
                },
                complete: function( xhr, status ) {
                    console.log( "Time request is complete!" );
                }
            });
        }
        function finish_test(){
            document.location.href='/knowtest/finish/?t_id='+Data.Initvalue;
        }
        $().ready(function(){
            read_questions();
            $('#b_prv').click(
                function(){
                    Data.cur_q--;
                    make_question_view();
                }
            );
            $('#b_nxt').click(
                function(){
                    Data.cur_q++;
                    make_question_view();
                }
            );
            $('#b_ans').click(
                function(){
                    fix_answer();
                }
            );
            c_time = setInterval('show_time()', 1000);
        })
