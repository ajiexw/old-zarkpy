/*
 * 	Sparker5 windowface03
 *	written by Sparker5 team
 *	http://sparker5.com
 *
 *	Built for Zark
 *	with cycle and fancybox, thanks!
 *
 *  include css:
 *      /plugins/sparker5/windowface/windowface03/windowface.css
 *      /plugins/jquery-plugins/fancybox/jquery.fancybox-1.3.4.css 
 *
 *  include js:
 *      /plugins/jquery-plugins/cycle.all.js
 *      /plugins/jquery-plugins/fancybox/jquery.mousewheel-3.0.4.pack.js
 *      /plugins/jquery-plugins/fancybox/jquery.fancybox-1.3.4.js
 *      /plugins/sparker5/windowface/windowface03/windowface.js 
 *
 *  html example:
 *      <div id="s5_windowface03" >
 *          <img src="/plugins/sparker5/windowface/windowface03/img/test1.jpg" alt="我是第1张图片的介绍"  />
 *          <img src_readly="/plugins/sparker5/windowface/windowface03/img/test2.jpg" alt="我是第2张图片的介绍"  />
 *          <img src_readly="/plugins/sparker5/windowface/windowface03/img/test3.jpg" alt="我是第3张图片的介绍"  />
 *      </div>
 *
 *  js example:
 *      $('#s5_windowface03').s5_windowface03({fancy_box: true});
 */

(function($) {

	$.fn.s5_windowface03 = function(options){
	  
		// default configuration properties
		var defaults = {			
            fx : 'scrollHorz',
            info_speed: 300,
            fancy_box: false,
            width:      '600px',
            height:      '230px',
            overlayOpacity    : 0.8,
            infoboxOpacity    : 0.8,
            fancybox_tip_image: '/plugins/sparker5/windowface/windowface03/img/fancybox_tip.png',
            left_arrow_image: '/plugins/sparker5/windowface/windowface03/img/arrow_left.png',
            right_arrow_image: '/plugins/sparker5/windowface/windowface03/img/arrow_right.png'
		}; 
		
		var options = $.extend(defaults, options);  

		this.each(function() {
			var obj = $(this);
            obj.width(options.width).height(options.height);

            obj.append('<div id="'+obj.attr('id')+'_slider" ></div>');
            $('img').addClass('s5_wf03_id_imgflow');
            $('img',obj).appendTo($('div#'+obj.attr('id')+'_slider',obj));

            obj.updateInfo = function(img_element){
                $('div#s5_wf03_infobox > p:eq(0)',obj).html($(img_element).attr('alt'));

                var index = 1;
                $('div#'+obj.attr('id')+'_slider',obj).find('img').each(function(i){
                    if ( this == img_element) index = i+1;
                });
                var count = $('div#'+obj.attr('id')+'_slider',obj).find('img').length;
                $('div#s5_wf03_infobox > p:eq(1)',obj).html(index+'/'+count);
            }

            options.after = function(currSlideElement, nextSlideElement, options, forwardFlag){
                obj.updateInfo(nextSlideElement);
                obj.current_img = nextSlideElement;
            }
            obj.current_img = $('> img',obj)[0]; //记录当前cycle轮播到的img，用于点击fancybox提示图标是触发fancybox
				
            obj.addClass('s5_windowface03').append('<img id="s5_wf03_fancybox_tip" src="'+options.fancybox_tip_image+'" class="s5_wf03_id_jumpicon" /> <img id="s5_wf03_prev" src="'+options.left_arrow_image+'" class="s5_wf03_id_switch_left" /> <img id="s5_wf03_next" src="'+options.right_arrow_image+'" class="s5_wf03_id_switch_right" />').append('<div id="s5_wf03_infobox" class="s5_wf03_id_infobox"> <p class="s5_wf03_id_infobox_title"></p><p class="s5_wf03_id_infobox_num"></p> </div>');
            options.prev = '#s5_wf03_prev'; //下一张按钮
            options.next = '#s5_wf03_next'; //上一张按钮
            $('#s5_wf03_infobox').animate({opacity:options.infoboxOpacity}); //infobox透明度
			
            $('div#'+obj.attr('id')+'_slider',obj).cycle(options);

            obj.out_run = null; //因为当图片滑动的时候会触发mouseover和mouseout事件，并且这两个事件的间隔很短，所以需要用一个30ms的延迟,如果某人的电脑特别卡怎么办？ 唉。。。
            obj.mouseover(function(){
                if (obj.out_run != null) {
                    clearTimeout(obj.out_run);
                    obj.out_run = null;
                }
                if (obj.in_arrow == false){ //如果obj.in_arrow==true,表示此事件是由鼠标进入左右箭头引起的，此时infobox已经show，所以可以不用show
                    $('#s5_wf03_infobox',obj).animate({bottom:'0px'},options.info_speed);
                    if (options.fancy_box == true){
                        $('#s5_wf03_fancybox_tip',obj).show();
                    }
                }
            }).mouseout(function(){
                obj.out_run = setTimeout(function(){
                    $('#s5_wf03_infobox',obj).animate({bottom:'-40px'},options.info_speed);
                    $('#s5_wf03_fancybox_tip',obj).hide();
                    obj.out_run = null;
                },30);
            });

            obj.in_arrow = false; //obj.in_arrow==true表示鼠标hover了左右箭头，此时禁用fancyBox
            if (options.fancy_box == true){
                $('#s5_wf03_prev,#s5_wf03_next').mouseover(function(){
                    $('#s5_wf03_fancybox_tip').hide();
                    obj.in_arrow = true;
                }).mouseout(function(){
                    $('#s5_wf03_fancybox_tip').show();
                    obj.in_arrow = false;
                });
            }
            obj.jsc = (new Date).getTime();
            if (options.fancy_box == true){
                $('div#'+obj.attr('id')+'_slider img',obj).each(function(){
                    $(this).wrap('<a href="'+$(this).attr('src')+'" titleinfo="'+$(this).attr('alt')+'" ></a>');//用titleinfo替代title是为了避免鼠标hover a标签时弹出title内容
                });
                $('div#'+obj.attr('id')+'_slider > a',obj).attr('rel','fancybox_group'+obj.jsc++).fancybox({
                    'transitionIn'		: 'none',
                    'transitionOut'		: 'none',
                    'titlePosition' 	: 'over',
                    'cyclic'            : true,
                    'overlayOpacity'    : options.overlayOpacity,
                    'titleFormat'		: function(title, currentArray, currentIndex, currentOpts) {
                        return '<span id="fancybox-title-over">' + $(currentArray[currentIndex]).attr('titleinfo') +  '</span>';
                    },
                    'onStart'           : function(){//pause cycle
                        $('div#'+obj.attr('id')+'_slider',obj).cycle('pause');
                    },
                    'onClosed'          : function(){//resume cycle
                        $('div#'+obj.attr('id')+'_slider',obj).cycle('resume');
                    }
                });
            }

            obj.updateInfo($('div#'+obj.attr('id')+'_slider',obj).find('img')[0]); //设置infobox的初始值
            $('#s5_wf03_fancybox_tip',obj).click(function(){
                $(obj.current_img).click();
            });
		});
	};
})(jQuery);
