/*
 *    Sparker5 Accordion01
 *    written by Sparker5 team
 *    http://sparker5.com
 *
 *    include js:
        <script type="text/javascript" src="/plugins/sparker5/accordion/accordion01/accordion.js"></script>
 *
 *    include css:
        <link rel="stylesheet" href="/plugins/sparker5/accordion/accordion01/accordion.css" type="text/css" media="screen" charset="utf-8"/>
 *
 *    example html:
 *      <div class="s5_accordion_01" >
 *          <ul>
 *              <li><a>category 1</a></li>
 *              <li><a>category 2</a></li>
 *              <li><a>category 3</a>
 *                  <div>
 *                      <ul>
 *                          <li><a>small 1</a></li>
 *                          <li><a>small 2</a></li>
 *                          <li><a>small 3</a></li>
 *                      </ul>
 *                  </div>
 *              </li>
 *          </ul>
 *      </div><div class="clearfix"></div>
 *     
 *     example js:
 *        $(".s5_accordion_01").s5_accordion_01();
 */

(function($) {

    $.fn.s5_accordion_01 = function(options){
      
        var defaults = {            
            speed       : 400,
            auto        : false,
            pause       : 0,
            right_img   : '/plugins/sparker5/accordion/accordion01/img/right.png',
            down_img    : '/plugins/sparker5/accordion/accordion01/img/down.png'
        }; 
        
        var options = $.extend(defaults, options);  
                
        this.each(function() {  
            var obj = $(this);                 
            /*set class*/
            $('> ul',obj).addClass('ul1')
            $('> ul > li',obj).addClass('li1')
            $('> ul > li > a',obj).addClass('a1')
            $('> ul > li > div',obj).addClass('div2')
            $('> ul > li > div > ul',obj).addClass('ul2')
            $('> ul > li > div > ul > li',obj).addClass('li2')
            $('> ul > li > div > ul > li > a',obj).addClass('a2')

            /*DOM  actions*/
            $('ul > li > div',obj).each(function(){
                var blind_div = $(this);
                $(this).prev('a').click(function(){
                    if (blind_div.css('display') == 'none'){
                        var click_a = $(this);
                        blind_div.show('blind',{},options.speed,function(){
                            click_a.next('span').hide();
                            blind_div.parent().attr('closed','true');
                        });
                    }else{
                        var click_a = $(this);
                        blind_div.hide('blind',{},options.speed,function(){
                            click_a.next('span').show();
                            blind_div.parent().attr('closed','false');
                            blind_div.parent().find('.span1').css("background","url("+options.down_img+") top right no-repeat");
                        });
                    }
                });
            });
            $('.a1',obj).after('<span class="span1"></span>').each(function(){
                if (($(this).attr('href') == undefined) || ($(this).attr('href').length == 0)){
                    $(this).attr('href','javascript:;');
                }
            });
            $('.a2',obj).after('<span class="span2"></span>');
            $('ul > li > div',obj).each(function(){
                if ($(this).css('display') != 'none'){
                    $(this).parent().find(' > span').hide();
                }
            });
            obj.width(obj.width()); //为了ie浏览器兼容性

            /*events for css*/
            $('.li1',obj).mouseover(function(){
                //如果此li没有子项son
                if ($(this).attr('has_son') != 'true') { 
                    //如果此li中的某个son被选中，则箭头不出现,否则箭头出现
                    if ( $(this).attr('selected') != 'son') {
                        $('.span1',$(this)).css("background","url("+options.right_img+") top right no-repeat");
                    }
                }else{//否则有子项
                    if ($(this).attr('closed') == 'true'){
                        $('.span1',$(this)).css("background","url("+options.down_img+") top right no-repeat");
                    }
                }
            }).mouseout(function(){
                if ($(this).attr('selected') != 'selected'){ //如果选中了此li，则箭头不消失,如果此li的某个son没选中，则此li必然不会被选中
                    $('.span1',$(this)).css("background","");
                }
            });

            $('.li2',obj).mouseover(function(){
                $('.span2',$(this)).css("background","url("+options.right_img+") top right no-repeat");
            }).mouseout(function(){
                if ($(this).attr('selected') != 'selected'){ //如果选中了此li，则箭头不消失
                    $('.span2',$(this)).css("background","");
                }
            });

            /*set selected*/
            /*
            $('.li1 > a',obj).each(function(){
                //如果此项默认被选中（即为当前页面）
                if ($(this).parent().attr('rich_name') === $.url(window.location.href).param('rich_name')){
                    $(this).parent().attr('selected','selected');
                    $(this).parent().find('.span1').css("background","url("+options.right_img+") top right no-repeat");
                }
            });
            $('.li2 > a',obj).each(function(){
                //如果此li有子项，且是收起的，closed=true,否则认为是展开的，closed=false
                if ($(this).parent().parent().parent().parent().attr('closed') == null) //加此if是为了避免其它子项重写closed
                    $(this).parent().parent().parent().parent().attr('has_son','true').attr('closed','true'); 
                //如果此项默认被选中（即为当前页面）
                if ($(this).parent().attr('rich_name') === $.url(window.location.href).param('rich_name')){
                    $(this).parent().attr('selected','selected');
                    $(this).parent().find('.span2').css("background","url("+options.right_img+") top right no-repeat");
                    $(this).parent().parent().parent().parent().find('.div2').show();
                    $(this).parent().parent().parent().parent().attr('selected','son').attr('closed','false');
                }
            });
            $('a',obj).each(function(){
                if (COMMON.isCurrentSite($(this).attr('href'))){
                    var href = $(this).attr('href');
                    href = $.url(href).setparam('rich_name',$(this).parent().attr('rich_name'));
                    $(this).attr('href',href);
                }
            });
            */
            
        });
    };

})(jQuery);
