/* 
* @Author: BlahGeek
* @Date:   2014-02-21
* @Last Modified by:   BlahGeek
* @Last Modified time: 2014-02-21
*/

$(document).ready(function(){

    var base_url = 'http://59.66.132.20:4242';

    $('#speak').click(function(e){
        e.preventDefault();
        var content = $('#content').val();
        if(content.length === 0) return;
        $('#content').val('');
        $.post(base_url + '/speak', {content: content});
    });

    var update_switch_status = function(){
        $.get(base_url + '/lightstatus', function(data){
            var $switch = $('#switch');
            $switch.data('on', data);
            if(data == '1')
                $switch.text('Turn Off Light');
            else
                $switch.text('Turn On Light');
        });
    };

    $('#switch').click(function(e){
        e.preventDefault();
        var $switch = $('#switch');
        var url = base_url;
        if($switch.data('on') == '1')
            url = base_url + '/turnoff505A';
        else
            url = base_url + '/turnon505A';
        $.get(url, update_switch_status);
    });

    update_switch_status();
    
});
