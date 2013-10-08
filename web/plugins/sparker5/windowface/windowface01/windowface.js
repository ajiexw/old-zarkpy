/*
 *
 * include css:
 *     /plugins/sparker5/windowface/windowface01/windowface.css
 *
 * include js:
 *     /plugins/jquery-plugins/cycle.all.js
 *     /plugins/sparker5/windowface/windowface01/windowface.js
 *
 * html example:
 *
 *     <div class="s5_windowface01">
 *         <div class="wf_wrap01 iepngfix"></div>
 *         <div class="wf_wrap02 iepngfix"></div>
 *         <div class="wf_showbox_img">
 *             $for showbox in showboxs:
 *                 <img src="$showbox.uri"/>
 *         </div>
 *         <div class="wf_switchbox">
 *             <div id="wf_windowface_nav" class="wf_switchbox_nav"></div>
 *         </div>
 *     </div>
 *
 * js example:
 *     $('.s5_windowface01').s5_windowface01();
 */

(function($) {
	$.fn.s5_windowface01 = function(options){
	  
		// default configuration properties
        var defaults = {			
            fx:         'fade',
            speed: 	    400,
            timeout:    4000,
            pager:      '#wf_windowface_nav',
            pause:	    1,
            slideExpr:  'img',
            callback:   null
        }; 
		
		var options = $.extend(defaults, options);  
				
		this.each(function() {
			var obj = $(this); 				
            obj.cycle({
                fx:     options.fx,
                speed:  options.speed,
                timeout: options.timeout,
                pager:  options.pager,
                pause:  options.pause,
                slideExpr: options.slideExpr
            });
            obj.addClass('sparker5_wf_01');

            // run callback
            $(options.pager+' a',obj).html('');
            if (options.callback != null){
                options.callback();
            } 
        });
	};

})(jQuery);
