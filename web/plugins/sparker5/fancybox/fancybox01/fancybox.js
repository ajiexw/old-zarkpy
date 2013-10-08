/*
 * 	Sparker5 fancybox01
 *	written by Sparker5 team
 *	http://sparker5.com
 *
 *	Built for Zark
 *	with fancybox, thanks!
 *
 *  include css: /plugins/jquery-plugins/fancybox/jquery.fancybox-1.3.4.css /plugins/sparker5/fancybox/fancybox01/fancybox.css 
 *  include js:  /plugins/jquery-plugins/fancybox/jquery.fancybox-1.3.4.js /plugins/sparker5/fancybox/fancybox01/fancybox.js 
 *
 *  example:
 *  <div id="s5_fancybox01" >
 *      <img src="/img/temp/Untitled-1.jpg" alt="我是第1张图片的介绍"  />
 *      <img src_readly="/img/temp/Untitled-3.jpg" alt="我是第2张图片的介绍"  />
 *      <img src_readly="/img/temp/Untitled-4.jpg" alt="我是第3张图片的介绍"  />
 *  </div>
 *  $('#s5_fancybox01').s5_fancybox01();
 */

(function($) {

	$.fn.s5_fancybox01 = function(options){
	  
		// default configuration properties
		var defaults = {			
            overlayOpacity    : 0.8,
            fancybox_tip_image: '/plugins/sparker5/fancybox/fancybox01/img/icon_openwindow.png',
            width:  '135px',
            height:  '135px'
		}; 
		
		var options = $.extend(defaults, options);

		this.each(function() {
			var obj = $(this);

            $('img',obj).each(function(){
                if ($(this).attr('src_readly') === undefined){
                    $(this).wrap('<a href="'+$(this).attr('src')+'" title="'+$(this).attr('alt')+'" ></a>');
                }else{
                    $(this).wrap('<a href="'+$(this).attr('src_readly')+'" title="'+$(this).attr('alt')+'" ></a>');
                }
            });

            obj.jsc = (new Date).getTime();
            $('a',obj).hide();
            $('a:eq(0)',obj).show();
            $('a',obj).attr('rel','fancybox_group'+obj.jsc++).fancybox({
                'transitionIn'		: 'none',
                'transitionOut'		: 'none',
                'titlePosition' 	: 'over',
                'cyclic'            : true,
                'overlayOpacity'    : options.overlayOpacity,
                'titleFormat'		: function(title, currentArray, currentIndex, currentOpts) {
                    return '<span id="fancybox-title-over">' + (title.length ? ' &nbsp; ' + title : '') +  '</span>';
                },
                'onStart'           : function(){
                    $('img[src_readly]',obj).each(function(){
                        $(this).attr('src',$(this).attr('src_readly'));
                    });
                }
            });

            obj.addClass('s5_fancybox01').append('<img src="'+options.fancybox_tip_image+'" class="s5_fb01_id_a_jumpicon" />');
            obj.width(options.width).height(options.height);

            $('.s5_fb01_id_a_jumpicon',obj).hide().click(function(){
                $('> a:eq(0)',obj).click();
            });
            obj.mouseover(function(){
                $('.s5_fb01_id_a_jumpicon',obj).show();
            }).mouseout(function(){
                $('.s5_fb01_id_a_jumpicon',obj).hide();
            });

		});
	};
})(jQuery);
