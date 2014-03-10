/* 
* @Author: BlahGeek
* @Date:   2014-02-21
* @Last Modified by:   BlahGeek
* @Last Modified time: 2014-03-10
*/

$(document).ready(function(){

    var base_url = '';

    $('#speak').click(function(e){
        e.preventDefault();
        var content = $('#content').val();
        if(content.length === 0) return;
        $('#content').val('');
        $.post(base_url + '/speak', {content: content});
    });

    var update_switch_status = function($switch, data){
        var d = parseInt(data);
        $switch.data('on', d);
        if(d == 1)
            $switch.text($switch.attr('data-msg-off'));
        else
            $switch.text($switch.attr('data-msg-on'));
    };

    $('.switch').click(function(e){
        e.preventDefault();
        var $switch = $(this);
        var url = base_url;
        if($switch.data('on') == 1)
            url = base_url + offpassword;
        else
            url = base_url + onpassword;
        $.get(url, {gpio: $switch.attr('data-gpio')}, function(data){
            update_switch_status($switch, data);
        });
    });

    var update_env = function(){
        $.get(base_url + '/env', function(data){
            if(data.indexOf('error') >= 0) return;
            var nums = $.trim(data).split('\n');
            $('#humidity').text(nums[0]);
            $('#temperature').text(nums[2]);
        });
        setTimeout(update_env, 60000);
    };

    update_env();

    $('.switch').each(function(i, v){
        var $switch = $(v);
        $.get(base_url + '/lightstatus', {gpio: $switch.attr('data-gpio')}, function(data){
            update_switch_status($switch, data);
        });
    });
    
});
