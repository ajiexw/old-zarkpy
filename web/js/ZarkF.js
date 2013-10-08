//ZARK's common function
(function(){


    var namespace = 'ZarkF';
    if (!window[namespace]) window[namespace] = {};
    var zark_functions = window[namespace];

    zark_functions.login = function(callback){
        ZarkAPI.isLogin({callback:function(data){
            if (data.state == true) callback();
            else zark_functions.pleaseLogin(callback);
        }});
    };

    var tfc = (new Date).getTime();
    zark_functions.buildLocalFuncion = function(cb){
        var local_function = namespace + tfc++;
        window[ local_function ] = function(data){
            cb & cb(data);
            zark_functions.deleteLocalFunction(local_function);//只能运行一次
        };
        return local_function;
    };

    zark_functions.deleteLocalFunction = function(local_function){
        window[ local_function ] = undefined;
        try{ delete window[ local_function ]; } catch(e){}
    };

    //弹出一个登录框，当用户成功登录后执行callback
    //前条件： ZarkF.isLogin() == false
    var login_box_id = 'login_box';
    var jump_register_box_id = 'jump_register_form';
    zark_functions.jump_login_callback = null;
    zark_functions.jump_register_callback = null;

    zark_functions.jumpLogin = function(){
        var post_data = {
            email:   $.trim($('#jump_login_form_email').val()),
            password:   $('#jump_login_form_password').val(),
            error:      $('#jump_login_error_tip'),
            rememberme: $('#jump_login_form input:checked[name=rememberme]').val()
        }
        $(this).blur();
        if (!post_data.email || post_data.email === 'Email'){
            post_data.error.html('请输入Email').show();
            return false;
        };
        if (!post_data.password || post_data.password === '密码'){
            post_data.error.html('请输入密码').show();
            return false;
        };
        zark_functions.tryLogin(post_data, zark_functions.jump_login_callback);
    };

    zark_functions.jumpRegister = function(){
        var post_data = {
            email:   $.trim($('#'+jump_register_box_id+' input[name=email]').val()),
            password:   $('#'+jump_register_box_id+' input[name=password]').val(),
            password2:  $('#jump_reg_password2').val(),
            email:      $.trim($('#'+jump_register_box_id+' input[name=email]').val()),
            sex:        $('#'+jump_register_box_id+' select[name=sex]').val(),
            error:      $('#jump_reg_error_tip')
        }
        $(this).blur();
        if (!post_data.email){
            post_data.error.html('请输入用户名.').show();
            return false;
        };
        if (!post_data.password){
            post_data.error.html('请输入密码.').show();
            return false;
        };
        if (post_data.password !== post_data.password2){
            post_data.error.html('两次输入的密码不相同.').show();
            return false;
        };
        if (!post_data.email){
            post_data.error.html('请输入邮箱地址.').show();
            return false;
        };
        zark_functions.tryRegister(post_data, zark_functions.jump_register_callback);
    };

    zark_functions.pleaseLogin = function(callback){
        var success_callback = zark_functions.buildLocalFuncion(callback);
        zark_functions.jump_login_callback = callback;
        $('#'+jump_register_box_id).hide();
        $('#jump_login_form').show();
        $('#overlayer').show();
        $('#'+login_box_id).fadeIn();
        //$('#jump_login_form input[name=email]').focus();
    };

    zark_functions.unpleaseLogin = function(callback){
        $('#'+login_box_id).hide();
        $('#overlayer').hide();
    };

    zark_functions.canclLogin = function(success_callback){
        zark_functions.deleteLocalFunction(success_callback);
        $('#'+login_box_id).remove();
    };

    zark_functions.loginSuccess = function(user_name, user_id, user_cover, success_callback){
        $('#'+login_box_id).fadeOut('fast');
        $('#overlayer').hide();
        $('<a href="/user/'+user_id +'"><img src="'+user_cover+'" class="user_img"/>'+user_name+'<em></em></a><ul id="user_nav"><li class="clearfix"><a href="/user/'+user_id +'" >个人主页</a></li><li class="clearfix"><a href="/accounts/share" style="color:#EB6478;" >邀请好友</a></li><li class="clearfix"><a href="/oauth/setting" >帐号绑定</a></li><li class="clearfix"><a href="/accounts" >帐号设置</a></li><li class="clearfix"><a href="/notice" >通知中心</a></li><li class="clearfix" ><a href="javascript:void(0);" onclick="ZarkF.logout();return false;">退出</a></li></ul>').appendTo('#login_info');


        $('#header_btn,#header_login_btn,#header_register_btn,#top_sina,#top_qq,#top_renren').hide();

        $('#login_info').show();

        success_callback && success_callback();
        zark_functions.setCookie('myid', user_id);
        zark_functions.showForMe();
        zark_functions.showForLeader();
        zark_functions.showForOthers();
        zark_functions.showForLogin();
    };

    zark_functions.showForMe = function(){
        if (zark_functions.getCookie('myid')){
            $('[showforme][showforme!='+zark_functions.getCookie('myid')+']').css('display', 'none');
            $('[showforme][showforme='+zark_functions.getCookie('myid')+']').css('display', 'block');
        }else{
            $('[showforme]').css('display', 'none');
        };
    };

    zark_functions.showForLeader = function(){
        if (zark_functions.getCookie('myid')){
            $('[showforleader][showforleader!='+zark_functions.getCookie('myid')+']').css('display', 'none');
            $('[showforleader][showforleader='+zark_functions.getCookie('myid')+']').css('display', 'block');
        }else{
            $('[showforleader]').css('display', 'none');
        };
    };


    zark_functions.showForOthers = function(){
        if (zark_functions.getCookie('myid')){
            $('[showforothers][showforothers='+zark_functions.getCookie('myid')+']').css('display', 'none');
            $('[showforothers][showforothers!='+zark_functions.getCookie('myid')+']').css('display', 'block');
        }else{
            $('[showforothers]').css('display', 'block');
        };
    };

    zark_functions.showForLogin = function(){
        if (zark_functions.getCookie('myid')){
            $('[showforlogin]').show();
            $('[showforunlogin]').hide();
        }else{
            $('[showforlogin]').hide();
            $('[showforunlogin]').show();
        };
    };
    zark_functions.tryLogin = function(post_data, success_callback){
        post_data.callback = function(data){
            if (data.is_login == true) {
                zark_functions.loginSuccess(data.user_name, data.user_id, data.user_cover, success_callback);
            }else{
                post_data.error.html('用户名或密码不对').show();
            };
        };
        zark_functions.clearCookies();
        ZarkAPI.login(post_data);
    };

    zark_functions.tryRegister = function(post_data, success_callback){
        post_data.callback = function(data){
            if (data.success == true) {
                zark_functions.loginSuccess(data.user_name, data.user_id, success_callback);
            }else{
                post_data.error.html(data.msg).show();
            };
        };
        ZarkAPI.register(post_data);
    };

    //删除元素
    zark_functions.remove = function(rubbish_selector){
        $(rubbish_selector).remove();
    };

    //刷新当前页面
    zark_functions.refresh = function(){
        window.location.reload();
    };

    $('a, input').click(function(){
        $(this).blur();
        return true;
    });

    zark_functions.setCookie = function(c_name,value,exdays)
    {
        $.cookie(c_name,value,exdays);
    };

    zark_functions.getCookie = function(c_name)
    {
        return $.cookie(c_name);
    };

    zark_functions.logout = function(){
        zark_functions.clearCookies();
        window.location.href = '/logout';
    };

    zark_functions.clearCookies = function(){
        zark_functions.setCookie('myid', null);
        zark_functions.setCookie('name', null);
        zark_functions.setCookie('email', null);
        zark_functions.setCookie('md5password', null);
    };

    zark_functions.getQueryString = function(name, url){
        if (!url) url = window.location.href;
        var reg = new RegExp("(^|\\?|&)"+ name +"=([^&]*)(\\s|&|$)", "i");
        if (reg.test(url)){
            return unescape(RegExp.$2.replace(/\+/g, " ")); 
        }else{
            return ""; 
        }
    };

})();
