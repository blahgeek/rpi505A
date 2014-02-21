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

    var update_switch_status = function(data){
        var $switch = $('#switch');
        var d = parseInt(data);
        $switch.data('on', d);
        if(d == 1)
            $switch.text('Turn Off Light');
        else
            $switch.text('Turn On Light');
    };

    $('#switch').click(function(e){
        e.preventDefault();
        var $switch = $('#switch');
        var url = base_url;
        if($switch.data('on') == 1)
            url = base_url + '/turnoff505A';
        else
            url = base_url + '/turnon505A';
        $.get(url, update_switch_status);
    });

    var update_env = function(){
        $.get(base_url + '/env', function(data){
            if(data.indexOf('error') > 0) return;
            var nums = $.trim(data).split('\n');
            $('#humidity').text(nums[0]);
            $('#temperature').text(nums[2]);
        });
    };

    setInterval(update_env, 60000);

    $.get(base_url + '/lightstatus', update_switch_status);
    
});
