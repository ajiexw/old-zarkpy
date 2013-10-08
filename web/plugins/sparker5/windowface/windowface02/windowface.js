/*
 * 	Sparker5 Fleaflea
 *	written by Sparker5 team
 *	http://sparker5.com
 *
 * include css:
 *     /plugins/sparker5/windowface/windowface02/windowface.css
 *     
 * include js:
 *     /plugins/jquery-plugins/cycle.all.js
 *     /plugins/sparker5/windowface/windowface02/windowface.js
 *
 * html example:
 *     <div class="s5_windowface02">
 *         <a href="http://baidu.com" ><img src="/img/temp/386.jpg"/></a>
 *         <a href="http://baidu.com" ><img src="/img/temp/387.jpg"/></a>
 *         <a href="http://baidu.com" ><img src="/img/temp/388.jpg"/></a>
 *     </div>
 *
 * js example:
 *     $('.s5_windowface02').s5_windowface02();
 *
 * tips:
 *     最后得到的高度比image_height参数多38个像素，做为control的高度
 * */


(function($) {
	$.fn.s5_windowface02 = function(options){
	  
        var defaults = {			
            fx:         'fade',
            width:      '930px',
            image_height:   '350px',
            speed: 	    400,
            timeout:    4000,
            pager:      '#wf_windowface_nav',
            pause:	    1, // hover时pause
            slideExpr:  'img'
        }; 
		
		var options = $.extend(defaults, options);  
				
		this.each(function() {
			var obj = $(this); 				
            var html = obj.html();
            obj.html('').width(options.width).height(options.image_height);
            obj.height(obj.height()+38);
            $('<div class="wf_showbox_img"></div>').html(html).appendTo(obj);
            $('<div class="wf_switchbox"> <div id="wf_windowface_nav" class="wf_switchbox_nav"></div> </div>').appendTo(obj);
        
            obj.cycle({
                fx:     options.fx,
                speed:  options.speed,
                timeout: options.timeout,
                pager:  options.pager,
                pause:  options.pause,
                slideExpr: options.slideExpr
            });

            $(options.pager+' a',obj).html(''); //delete number table
            // set css attribute
            $('.wf_showbox_img img',obj).height(options.image_height);
            $('.wf_switchbox ',obj).css('top',$('.wf_showbox_img img').height()+10+'px');
        });
	};
})(jQuery);
