// Feed App related Javascript

// Getting CSRF token from cookie

$(document).ready(function() {
	// body...
	function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method){
    	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
    }

    $.ajaxSetup({
    	beforeSend: function(xhr, settings){
    		if(!csrfSafeMethod(settings.type) && !this.crossDomain){
    			xhr.setRequestHeader("X-CSRFToken", csrftoken);
    		}
    	}
    });

  //        var csrftoken = getCookie('csrftoken');
	 //     // if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) 
	 //     	if (!this.crossDomain){
	 //             // Only send the token to relative URLs i.e. locally.
	 //             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	 //         }
	 //     } 
		// });
});

// Feed post form handling the post button 

$(document).ready(function() {
    // Changing the Input size of the feed form dynamically on click and on blur
    $('#id_post_info').click(function(){
        $('#id_post_info').css({
            'height':'75px',
        });
        // on blur 
    }).blur(function(){
        $('#id_post_info').css({
            'height':'25px',
        });
    });

    $('#feed_form_submit').prop('disabled', true);
    function validatePostData(){
        // console.log($('#id_image').get(0).files.length !== 0)
        var postData = $('#id_post_info').val() !== '' || $('#id_image').get(0).files.length !== 0 || $('#id_video').get(0).files.length !==0 ;
        // console.log(!postData)
        $('#feed_form_submit').prop('disabled', !postData);
    }
    // call the validatePostData function when there is keyup in input text
    $('#id_post_info').on('keyup', validatePostData);
    // call the validatePostData function when user inputs the image file
    $('#id_image').change(validatePostData);
    // call the validatePostData function when user inputs the Video file
    $('#id_video').change(validatePostData);
});


// Handling the Likes section with the JQuery and Ajax
$(document).ready(function(){
    // function updateText(btn, count, verb) {
    //     btn.text(count) 
    // }
    $('.likes_form').on('submit', function (event){
        event.preventDefault();
        // console.log('Likes working')
        // var this_ = $("span[class='likes_value small']", this);
        $.ajax({
            type:$(this).attr('method'),
            context:this,
            url : $(this).attr('likes-url'),
            data : $(this).serialize(),
            success: function(data){
                var count;
                // console.log(this);
                count = data.count;
                if(count==0){
                    $(this).find('.likes_value').empty();
                }else{
                // updateText(this_, count, "Likes")
                // console.log($(this).find('input[class="likes_btn"]').add("<h2>2</h2>"));
                // $(this).find('input[class="likes_btn"]').add("<h2>2</h2>");
                $(this).find('.likes_value').text(count);
                }
            },
            error: function(data) {
                alert('something wrong')
            }
        });
    });
});

// Handling the comment section with the JQuery and Ajax
$(document).ready(function(){
    $('.comment_form').on('submit', function(event){
        event.preventDefault();
        // console.log('working')
        var this_c = $("input[type=text]",this)
        $.ajax({
            type:$(this).attr('method'),
            context:this,
            url: $(this).attr('comment-url'),
            data: $(this).serialize(),
            success: function(data){
                var url_val;
                url_val = data.url_val;
                $(this).find('.comment_btn').blur();
                $(this_c).val("");
                // if logged in user and commenting user same
                if(data.value){
                    // if(data.fname_empty){
                        $(data.id).prepend("<li class='list-group-item p-0 comment_li' id='"+data.oid+"'><div class='d-flex flex-row child_comm_dv'><div class='comment_user'><a class='small pr-1' href='"+url_val+"'>"+data.user+"</a></div><div class='d-flex flex-column'><div class='d-flex flex-row'><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div><div class='d-flex flex-row reply_div'><div class='comm_rply_div'><span class='btn btn-link comment_reply'>Reply</span></div><div class='comm_lik_div'><span class='btn btn-link comment_likes'>Likes</span><span class='comm_lik_val'></span></div></div></div></div></li>");
                        // console.log("<li class='list-group-item p-0'><small><a href="+url_val+">"+data.user+"</a>"+data.comments+"</small></li>")
                    // }
                    // // Updating the Comment Username as per the first_name saved in DB
                    // else{
                    //     // console.log('first else')
                    //     $(data.id).prepend("<li class='list-group-item p-0' id='"+data.oid+"'><div class='d-flex flex-row'><a class='small pr-1' href='"+url_val+"'>"+data.user+"</a><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></li>")
                    // }
                }
                // if the logged in user and commenting user are different
                else{
                    // // console.log("in else")
                    // if(data.fname_empty){
                    //     $(data.id).prepend("<li class='list-group-item p-0' id='"+data.oid+"'><div class='d-flex flex-row'><a class='small pr-1' href='"+url_val+"'>"+data.user+"</a><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></li>")
                    // }
                    // // Updating the Comment Username as per the first_name saved in DB
                    // else{
                        // console.log('second else')
                        $(data.id).prepend("<li class='list-group-item p-0 comment_li' id='"+data.oid+"'><div class='d-flex flex-row child_comm_dv'><div class='comment_user'><a class='small pr-1' href='"+url_val+"'>"+data.user+"</a></div><div class='d-flex flex-column'><div class='d-flex flex-row'><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div><div class='d-flex flex-row reply_div'><div class='comm_rply_div'><span class='btn btn-link comment_reply'>Reply</span></div><div class='comm_lik_div'><span class='btn btn-link comment_likes'>Likes</span><span class='comm_lik_val'></span></div></div></div></div></li>");
                        // $(data.id).prepend("<li class='list-group-item p-0' id='"+data.oid+"'><div class='d-flex flex-row'><a class='small pr-1' href='"+url_val+"'>"+data.user+"</a><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></li>")
                    // }
                }
            },
        });
    });
});

// Editing the comment section belongs to the Feed App

// Clicking on the Edit button of comment
$(document).ready(function(){
    // Editing the already posted comment
    $('.post_edit_parent').on('click', '.edit_button', function(){
        var comment_value = $(this).parents('li').find('.span_dimen').text();
        // console.log(comment_value);
        // console.log(this);

        $(this).parents('li').find('.span_dimen').replaceWith("<form class='comm-update-form' class='p-1' method='post'><input name='comments' class='comment_ip' type='text'><input class='correct_img' type='image' src='/static/components/Correct.png'><input type='image' class='cancel_img' src='/static/components/Cancel.png'></form>");
        $('.comment_ip').css({
            'width':'230px',
            'height': '50px',
            'font-size':'12px',
            'word-wrap': 'break-word',
            'word-break':'break-all'

        });
        $('.correct_img').css({
                'width': '30px',
                'height':'30px'
        });
        $('.cancel_img').css({
                'width': '30px',
                'height':'30px'
        });
        $(this).hide();
        $(this).parents('li').find('input[class="comment_ip"]').attr('value', comment_value).focus();

        // Cancel X to replace the existing comment data
        $('.cancel_img').on('click', function(event){
            event.preventDefault();
            this_ = $(this);
            var edit = $(this).parents('li').find('.edit_button:hidden');
            $(this).closest('.comm-update-form').replaceWith('<span class="small span_dimen pr-1">'+comment_value+'</span>');
            $(edit).show();

        });

    });
    // submitting or updating the comment data to the server and re-displaying dynamically the data from server
    $('ul').on('submit', '.comm-update-form', function(e){
        e.preventDefault();
        var ider = $(this).parents('li').attr('id');
        var comment_form = $(this);
        var edit_ = $(this).parents('li').find('.edit_button:hidden');
        // console.log('comment_update/'+ider+'/');
            $.ajax({
                context: this,
                url: 'comment_update/'+ider+'/',
                type: comment_form.attr('method'),
                data: comment_form.serialize(),
                success: function(data){
                    $(this).replaceWith('<span class="small span_dimen pr-1">'+data.comment_val+'</span>');
                    $(edit_).show();
                }
            });

    });
});

// Edit post Dynamically belongs to Feed App

// This section covers posting, cancelling and displaying the feed_post dynamically
$(document).ready(function(){
    $('.post_edit_parent').on('click','.post_edit', function(event){
        event.preventDefault();
        // console.log($(this).parents('div .row'));
        // .children('.replaced_editor').find('.post_info').text());
        var post_info_get = $(this).parents('div .row').find('.post_info').size();
        var img_url_get = $(this).parents('div .row').find('.post_img_url').size();
        // console.log($(this).parents('div .row').find('.post_img_url')); 
        var vdo_url_get = $(this).parents('div .row').find('video').size();
        var feed_id = $(this).parents('div .row').find('.replacer_editor').attr('id');

        // console.log(1,img_url_get);
        // console.log(2,post_info_get);
        // console.log(3,vdo_url_get);

        if(img_url_get !== 0){
            var img_url = $(this).parents('div .row').find('.post_img_url').attr('src');
            // console.log(img_url)
        }else{
            // console.log('here..?')
            var img_url = '';
        }
        if(vdo_url_get !== 0 ){
            var vdo_url = $(this).parents('div .row').find('source').attr('src');
        }else{
            var vdo_url = '';
        }
        if(post_info_get !== 0){
            var post_info = $(this).parents('div .row').find('.post_info').text();
        }
        // else{
        //  var post_info = '';
        // }

        var replacer_editor = $(this).parents('div .row').find('.replacer_editor').html();
        
        $(this).parents('div .row').find('.replacer_editor').load('/static/fe.html #p_ed_dat_r', function(){
            // console.log($(this).parents('.dyn_edit_cont').find('.input_post_file_iedit').attr('id',feed_id+'_img_id'));
            $(this).parents('.dyn_edit_cont').find('.input_post_file_iedit').attr('id',feed_id+'_img_id');
            $(this).parents('.dyn_edit_cont').find('label[for="id_for_image"]').attr('for',feed_id+'_img_id');
            $(this).parents('.dyn_edit_cont').find('.input_post_file_vedit').attr('id',feed_id+'_vdo_id');
            $(this).parents('.dyn_edit_cont').find('label[for="id_for_video"]').attr('for',feed_id+'_vdo_id');
            if(img_url_get == 0){
            $(this).parents('div .row').find('.img_cont').hide();
            } else{
                $(this).find('.img_cont').attr('src',img_url);
            }
            if(vdo_url_get==0){
                $(this).find('video').hide();
            }else{
                $(this).find('source').attr('src',vdo_url);
            }
            if(post_info_get.length <= 1){
                $(this).find('.post_ip_txt').hide();
            }else{
                $(this).find('.post_ip_txt').attr('value',post_info);
                $(this).find('.post_ip_txt').css({'border':'none'}).focus();
            }

        });

    });
    // Cancelling the edit action of dynamic edit
    $('.dyn_edit_cont').on('click','#pe_cancel_btn', function(){
        // console.log(this);
        var feed_id = $(this).parents('.replacer_editor').attr('id');

        $.ajax({
            url:'edit/'+feed_id+'/',
            context:this,
            type:'GET',
            success: sucAndCan,
            error:function(){
                console.log('is it failing..?')
            }
        });
    });

    // Submit or updating dynamically the post data
    $('.dyn_edit_cont').on('submit', '.re_post', function(event){
        event.preventDefault();
        var form = new FormData($(this)[0]);
        var feed_id = $(this).parents('.replacer_editor').attr('id');
        // console.log($(this).attr('method'));
        // console.log($(this)[0]); 
        // console.log(form);
        // console.log($(this).parents('.replacer_editor').find('.input_post_file_iedit'));

        $.ajax({
            url:'edit/'+feed_id+'/',
            context:this,
            type: $(this).attr('method'),
            data: form,
            contentType: false,
            processData: false,
            success: sucAndCan,
        });
    });
    
    // which is called by both cancel and update btn of dynamic edit post
    function sucAndCan(data){
        // console.log($(this));
            var main_div = $(this).parents('.replacer_editor');
            $(this).parents('.replacer_editor').empty().load('/static/fe.html #p_ed_dat_a', function(){

                if(data.image !== ''){
                    var img_url = $(this).find('img').attr('src', data.image);
                    // console.log(img_url)
                }
                else{
                    // console.log('here..?')
                    $(this).find('img').remove();
                }

                if(data.video !== '' ){
                    var vdo_url = $(this).find('source').attr('src',data.video);
                    // console.log('why..?');
                }
                else{
                    $(this).find('video').remove();
                }

                if(data.post_info !== ''){
                    var post_info = $(this).find('span').text(data.post_info);
                }else{
                $(this).find('span').remove();
            }

        });
    }

   
}); //document.ready closure

// Preview of the Images and Video files during the post edit
$(function(){
     $('.dyn_edit_cont').on('change','.input_post_file_iedit, .input_post_file_vedit',function(){
        // console.log($(this).parents('.replaced_editor').find('.img_cont'));
        if(this.files && this.files[0]){
            // console.log(this);
            if(this.files[0].type.startsWith('image/')){
                // console.log(this.files[0].type);
                // console.log($(this).parents('div .row').find('.img_cont'))
                $(this).parents('.dyn_edit_cont').find('.img_cont').attr('src', URL.createObjectURL(this.files[0])).show();
                $(this).parents('.dyn_edit_cont').find('.img_cont').onload = function(){
                    URL.revokeObjectURL(this.src);
                }
            }
            else if(this.files[0].type.startsWith('video/')){
                // console.log(this.files[0].type);
                // console.log($(this).parents('.dyn_edit_cont').find('video'));
                $(this).parents('.dyn_edit_cont').find('video').attr('src', URL.createObjectURL(this.files[0])).show();
                $(this).parents('.dyn_edit_cont').find('video').onload = function(){
                    URL.revokeObjectURL(this.src);
                }
            }
            else{
                console.log(this.files[0].type);
                 alert('Please select the proper image file');
            }
            
        }

    });

});

$(function(){

    function readURL() {
        //  rehide the image and remove its current "src",
        //  this way if the new image doesn't load,
        //  then the image element is "gone" for now
        $('#fi_disp').attr('src', '').hide();
        if (this.files && this.files[0]) {

            if(this.files[0].type.startsWith('image/')){
                $('#fi_disp').attr('src', URL.createObjectURL(this.files[0]));
                $('#fi_disp').onload = function(){
                    URL.revokeObjectURL(this.src);
                }
            }else if(this.files[0].type.startsWith('video/')){
                // $('#id_video').attr()
                var video = $('#vdo_post_prvw');
                // console.log($('#vdo_post_prvw source').attr('src'));
                // console.log($('video'))
               

                $('#vdo_post_prvw source').attr('src', URL.createObjectURL(this.files[0]));
                 $(video).css({
                    'width':'400px',
                    'height':'250px',
                    'display':'inline',
                });
                // console.log(this.src)
                // , $('#vdo_post_prvw source').attr('src')); 
                $('#vdo_post_prvw')[0].load();
                // console.log(this.src)
                // , $('#vdo_post_prvw source').attr('src'));
                // $('#vdo_post_prvw').onload = function(){
                //     // $('#vdo_post_prvw').get(0).play();
                // console.log(this.src, $('#vdo_post_prvw source').attr('src'));
                // URL.revokeObjectURL(this.src);
                // console.log(this.src, $('#vdo_post_prvw source').attr('src'));
                // }
            }

            // var reader = new FileReader();
            // $(reader).load(function(e) {
            //  $('#fi_disp')
            //      //  first we set the attribute of "src" thus changing the image link
            //      .attr('src', e.target.result)   //  this will now call the load event on the image
            // });
            // reader.readAsDataURL(this.files[0]);

        }
    }

    //  below makes use of jQuery chaining. This means the same element is returned after each method, so we don't need to call it again
    $('#fi_disp')
        //  here we first set a "load" event for the image that will cause it change it's height to a set variable
        //      and make it "show" when finished loading
        .load(function(e) {
            // e.preventdefault();
            //  $(this) is the jQuery OBJECT of this which is the element we've called on this load method
            $(this)
                //  note how easy adding css is, just create an object of the css you want to change or a key/value pair of STRINGS
                .css('height', '400px') //  or .css({ height: '200px' })
                //  now for the next "method" in the chain, we show the image when loaded
                .show();    //  just that simple
            $(this).css('width', '400px').show();
        })
        //  with the load event set, we now hide the image as it has nothing in it to start with
        .hide();    //  done

$("#id_image").change(readURL);
$('#id_video').change(readURL);

});

// Image and Video slider display
$(function(){
    // On Next Image/Video click
    // $()
    $('.post_edit_parent').on('click', '.next', function(){
        
        var currentElement = $(this).parents('.outer_container').find('.active');
        var demo = $(this).parents('.outer_container').find('.demo');
        // console.log(demo);
        if($(currentElement).get(0).nodeName == 'VIDEO'){
            $(currentElement)[0].currentTime = 0;
            $(currentElement)[0].pause();
        }
        var nextElement = currentElement.next();
        if(nextElement.length){
            if($(nextElement).get(0).nodeName == 'VIDEO'){
                $(nextElement).get(0).play();
            }
            // console.log('inside clicked')
            currentElement.removeClass('active').css('z-index', -10);
            nextElement.addClass('active').css('z-index',10);
            // console.log($(demo).next().get(0));
            demo.removeClass('w3-white');
            $(demo).next().addClass('w3-white');
            // console.log($(this).parents('.outer_container').find('.demo'))
        }    
    });
    // On Previous image/video display
    $('.post_edit_parent').on('click','.prev', function(){
        // console.log('you are hitting me');
        var currentElement = $(this).parents('.outer_container').find('.active');
        var demo = $(this).parents('.outer_container').find('.demo');
        // console.log('here', currentElement);
        if($(currentElement)[0].nodeName == 'VIDEO'){
            // console.log(currentElement[0].currentTime);
            $(currentElement)[0].currentTime = 0;
            $(currentElement)[0].pause();
        }
        var prevElement = currentElement.prev();

        if(prevElement.length){
            currentElement.removeClass('active').css('z-index', -10);
            prevElement.addClass('active').css('z-index',10);
            demo.removeClass('w3-white');
            demo.prev().addClass('w3-white');
        }

    })
});


$(function(){
    // Handling the likes of parent Comments
    $('.post_edit_parent').on('click','.comment_likes', function(event){
        event.preventDefault();
        var comment_id = $(this).parents('.list-group-item').attr('id');
        // console.log(comment_id);

        $.ajax({
            context:this,
            url:'cl/'+comment_id+'/',
            data: {'likes':1},
            type:'post',
            success:function(data){
                // console.log(this);
                if(data.likes == 0){
                    $(this).next('.comm_lik_val').empty();
                }else{
                    $(this).next('.comm_lik_val').text(data.likes);
                    // $(this).empty().text('Likes').append('<span>'+data.likes+'</span>');
                }
                
            }

        });
    });

    // Handling likes of the child comments
    $('.post_edit_parent').on('click','.c_comment_likes', function(event){
        event.preventDefault();
        var comment_id = $(this).parents('.child_comm_dv').attr('id');
        // console.log(comment_id);

        $.ajax({
            context:this,
            url:'rcl/'+comment_id+'/',
            data: {'likes':1},
            type:'post',
            success:function(data){
                // console.log(this);
                if(data.likes == 0){
                    $(this).next('.comm_lik_val').empty();
                }else{
                    $(this).next('.comm_lik_val').text(data.likes);
                    // $(this).empty().text('Likes').append('<span>'+data.likes+'</span>');
                }
                
            }

        });
    });


    // Handling the comment of comments section
    $('.post_edit_parent').on('click', '.comment_reply', function(event){
        event.preventDefault();
        // console.log($(this).parents('li').find('.reply_div'));
        // console.log($(this).parents('li').find('.reply_div').siblings('.com_com_div'));
        // ;'.comm_comm_form'));
        if($(this).parents('li').find('.reply_div').siblings(".com_com_div").length == 1){
            // console.log('Will hide');
            $(this).parents('li').find('.reply_div').siblings(".com_com_div").remove();
        }else{
        $(this).parents('li').find('.reply_div').after("<div class='com_com_div d-flex flex-row'><form class='com_comm_form' method='post'><input type='text' name='related_comment' class='rc_ip'><input class='correct_img' type='image' src='/static/components/Correct.png'></form><input type='image' class='cancel_img' src='/static/components/Cancel.png'></div>");
        $(this).parents('li').find('.rc_ip').focus();
        // console.log($(this).parents('li').find('.rc_ip'));
        }
    });

    // Handling the children comments new form section
    $('.post_edit_parent').on('click', '.ch_cc_reply', function(event){
        event.preventDefault();
        // console.log($(this).parents('.pa_ch_div'));
        // console.log($(this))
            // .find(''));
        // console.log($(this).parents('.child_comm_dv').find('').siblings('.com_com_div'));
        // ;'.comm_comm_form'));
        if($(this).parents('.child_comm_dv').find('.cc_reply_div').siblings(".com_com_div").length == 1){
            // console.log('Will hide');
            $(this).parents('.child_comm_dv').find('.cc_reply_div').siblings(".com_com_div").remove();
        }else{
        $(this).parents('.child_comm_dv').find('.cc_reply_div').after("<div class='com_com_div d-flex flex-row'><form class='comm_comm_form' method='post'><input type='text' name='related_comment' class='rcc_ip'><input class='correct_img' type='image' src='/static/components/Correct.png'></form><input type='image' class='cancel_img' src='/static/components/Cancel.png'></div>");
        $(this).parents('.child_comm_dv').find('.rc_ip').focus();
        // console.log($(this).parents('li').find('.rc_ip'));
        }
    });


    // Submit the data comments of the comments on parent reply
    $('.post_edit_parent').on('submit','.com_comm_form', function(event){
        event.preventDefault();
        // console.log($(this).parents('li').attr('id'));
        var id = $(this).parents('li').attr('id');
        $.ajax({
            context:this,
            url: 'rc/'+id+'/',
            type: 'post',
            data: $(this).serialize(),
            success: function(data){
                var parnt_dv = $(this).parents('.com_com_div');
                    $(this).parents('.com_com_div').load('/static/fe.html #commentOfcomment', function(){
                        $(parnt_dv).find('.c_comment_user').text(data.a_value);
                        $(parnt_dv).find('.c_span_dimen').text(data.comments);
                        $(parnt_dv).find('.child_comm_dv').attr('id',data.id);

                    });
            },
            error:function(e){
                console.log(e);
            }

        });
    });

        // Submit the data comments of the comments on children reply 
    $('.post_edit_parent').on('submit','.comm_comm_form', function(event){
        event.preventDefault();
        // console.log($(this).parents('li').attr('id'));
        var id = $(this).parents('li').attr('id');
        console.log($(this).find('.rcc_ip').val());
        if($(this).find('.rcc_ip').val()){
        $.ajax({
            context:this,
            url: 'rc/'+id+'/',
            type: 'post',
            data: $(this).serialize(),
            success: function(data){
                var parnt_dv = $(this).parents('.pa_ch_div');
                // console.log($(this).parents('.pa_ch_div').append("<div id='dumm'></div>"));
                $(parnt_dv).append("<div id='dumm'></div>");
                $(this).parents('.com_com_div').remove();

                $(parnt_dv).find('#dumm').load('/static/fe.html #commentOfcomment', function(){
                        console.log('am I here.?');
                        // $(parnt_dv).find('#dumm').html($(data).find('#commentOfcomment').html());
                        console.log($(parnt_dv).children('#dumm').find('.c_comment_user'));
                        $(parnt_dv).children('#dumm').find('.c_comment_user').text(data.a_value);
                        $(parnt_dv).children('#dumm').find('.c_span_dimen').text(data.comments);
                        $(parnt_dv).children('#dumm').find('.child_comm_dv').attr('id',data.id);
                        console.log($(parnt_dv).children('#dumm').attr('id'));
                        $(parnt_dv).children('#dumm').attr('id','dumm'+data.id);
                });
            },
            error:function(e){
                console.log(e);
            }

        });
        }else{
            alert('Enter the value');
        }   
    });

    // Cancel action for empty form which is generated by reply button
    $('.post_edit_parent').on('click','.cancel_img', function(){
        // console.log(this);
        $(this).parents('.com_com_div').remove();
    });

    // Edit section of the existing comment posted by the user
    $('.post_edit_parent').on('click', '.c_edit_button', function(){
        var comment_value = $(this).siblings('.c_span_dimen').text();

        $(this).siblings('.c_span_dimen').replaceWith("<form class='com_comm_form' class='p-1' method='post'><input name='related_comment' class='c_comment_ip' type='text'><input class='correct_img' type='image' src='/static/components/Correct.png'><input type='image' class='cancel_img' src='/static/components/Cancel.png'></form>");
        $('.comment_ip').css({
            'width':'230px',
            'height': '50px',
            'font-size':'12px',
            'word-wrap': 'break-word',
            'word-break':'break-all'

        });
        $('.correct_img').css({
                'width': '30px',
                'height':'30px'
        });
        $('.cancel_img').css({
                'width': '30px',
                'height':'30px'
        });
        $(this).hide();
        $(this).siblings('.com_comm_form').find('input[class="c_comment_ip"]').attr('value', comment_value).focus();

        // Cancel X to replace the existing comment data
        $('.cancel_img').on('click', function(event){
            event.preventDefault();
            this_ = $(this);
            var edit = $(this).parent('.com_comm_form').parent('.flex-row').find('.c_edit_button:hidden');
            // console.log($(this).parent().);
            $(this).closest('.com_comm_form').replaceWith('<span class="small c_span_dimen pr-1">'+comment_value+'</span>');
            $(edit).show();

        });


        // Posting the updated comment to the server and updating the div post success
        $('.post_edit_parent').on('click','.correct_img', function(event){
        event.preventDefault();
        // console.log($(this).parents('li').attr('id'));
        var id = $(this).parents('.child_comm_dv').attr('id');
        var form = $(this).parents('.child_comm_dv').find($('.com_comm_form'));
        // console.log(form)
        $.ajax({
            context:this,
            url: 'rcu/'+id+'/',
            type: 'post',
            data: form.serialize(),
            success: function(uc_data){
                    // $(this).parents('.com_com_div').load('/static/fe.html #commentOfcomment', function(){
                        var btn = $(this).parents().siblings('.c_edit_button:hidden');
                        $(this).parents('.com_comm_form').replaceWith('<span class="small c_span_dimen pr-1">'+uc_data.rc+'</span>');
                        $(this).parents().siblings('.c_edit_button:hidden').show();
                        $(btn).show()
                        // console.log($(btn));
            },
            error:function(e){
                console.log(e);
            }

        });
    });
    });
});
