/*
 *  Sparker5 Pagination01
 *  written by Sparker5 team
 *  http://sparker5.com
 *
 *  include css:
 *      /plugins/sparker5/pagination/pagination01/pagination.css
 *  include js:
 *      /plugins/jquery-plugins/url.js /plugins/sparker5/pagination/pagination01/pagination.js
 *  html example:
 *      <div class="s5_pagination01">
 *          <input type="hidden" name="max"  value="20"/>
 *          <input type="hidden" name="page_num"  value="1"/>
 *          <input type="hidden" name="displaycount"  value="10"/>
 *          <input type="hidden" name="firsttext"  value="第一页"/>
 *          <input type="hidden" name="lasttext"  value="末页"/>
 *      </div>
 *
 *  js example:
 *      $('.s5_pagination01').s5_pagination01();
 */

(function($) {

    $.fn.s5_pagination01 = function(options){
      
        var defaults = {
                text_color                : '#79B5E3',
                background_color          : 'none',
                text_hover_color          : '#2573AF',
                background_hover_color    : 'none'
        }; 
        
        var options = $.extend(defaults, options);  

        var namespace ="s5_pagination01";
        if (!window[namespace]){
            window[namespace] = {};
        }
        var s5_pagination01 = window[namespace];

        this.each(function(){  
            var obj = $(this);
            var max = parseInt($('input[name=max]',obj).val());
            var page_num = parseInt($('input[name=page_num]',obj).val());
            var displaycount = parseInt($('input[name=displaycount]',obj).val());
            var firsttext = $('input[name=firsttext]',obj).val();
            var lasttext = $('input[name=lasttext]',obj).val();
            obj.addClass('s5_pagination01').html('');
            var pagination_html = '';
            pagination_html += '<ul>'

            var start = Math.max(0,page_num - Math.ceil(displaycount/2));
            var end = start + displaycount;
            if(end>max){
                end = max;
                start = Math.max(0,max - displaycount);
            }

            if (page_num !== 1){
                pagination_html += '<li page_num="1">'+firsttext+'</li>';
            }else{
                pagination_html += '<li >'+firsttext+'</li>';
            }

            for(var i=start;i<end;i++){
                if (i+1==page_num){
                    pagination_html += '<li class="current_page">'+(i+1)+'</li>';
                }else{
                    pagination_html += '<li page_num="'+(i+1)+'" >'+(i+1)+'</li>';
                }
            }

            if (page_num !== max){
                pagination_html += '<li page_num="'+max+'">'+lasttext+'</li>';
            }else{
                pagination_html += '<li>'+lasttext+'</li>';
            }

            pagination_html += '</ul>'
            obj.append(pagination_html);
            // click event
            $('li[page_num]',obj).each(function(){
                var href = $.url(window.location.href);
                $(this).html('<a href="'+href.setparam('page_num',$(this).attr('page_num'))+'">'+$(this).html()+'</a>');
            });
        });
    };
})(jQuery);
