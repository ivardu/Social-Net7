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
    function updateText(btn, count, verb) {
        btn.text(count) 
    }
    $('.likes_form').on('submit', function (event){
        // console.log('Likes working')
        event.preventDefault();
        var this_ = $("span[class='likes_value small']", this);
        $.ajax({
            type:$(this).attr('method'),
            url : $(this).attr('likes-url'),
            data : $(this).serialize(),
            success: function(data){
                var count;
                // console.log(data.count)
                count = data.count
                updateText(this_, count, "Likes")
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
        // console.log('working')
        var this_c = $("input[type=text]",this)
        event.preventDefault();
        $.ajax({
            type:$(this).attr('method'),
            url: $(this).attr('comment-url'),
            data: $(this).serialize(),
            success: function(data){
                var url_val;
                url_val = data.url_val
                $('#comment_btn').blur();
                $(this_c).val("");
                // if logged in user and commenting user same
                if(data.value){
                    if(data.fname_empty){
                        $(data.id).prepend("<li class='list-group-item p-0'><div class='d-flex flex-row'><a class='small' href='"+url_val+"'>"+data.user+"</a><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></li>")
                        // console.log("<li class='list-group-item p-0'><small><a href="+url_val+">"+data.user+"</a>"+data.comments+"</small></li>")
                    }
                    // Updating the Comment Username as per the first_name saved in DB
                    else{
                        // console.log('first else')
                        $(data.id).prepend("<li class='list-group-item p-0'><div class='d-flex flex-row'><a class='small' href='"+url_val+"'>"+data.user+"</a><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></li>")
                    }
                }
                // if the logged in user and commenting user are different
                else{
                    // console.log("in else")
                    if(data.fname_empty){
                        $(data.id).prepend("<li class='list-group-item p-0'><div class='d-flex flex-row'><a class='small' href='"+url_val+"'>"+data.user+"</a><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></li>")
                    }
                    // Updating the Comment Username as per the first_name saved in DB
                    else{
                        // console.log('second else')
                        $(data.id).prepend("<li class='list-group-item p-0'><div class='d-flex flex-row'><a class='small' href='"+url_val+"'>"+data.user+"</a><span class='small span_dimen pr-1'>"+data.comments+"</span> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></li>")
                    }
                }
            },
        });
    });
});

// Editing the comment section belongs to the Feed App

// Clicking on the Edit button of comment
$(document).ready(function(){
    // Editing the already posted comment
    $('ul').on('click', '.edit_button', function(){
        var comment_value = $(this).parent().children('span').text();

        $(this).parents('li').find('span').replaceWith("<form class='comm-update-form' class='p-1' method='post'><input name='comments' class='comment_ip' type='text'><input class='correct_img' type='image' src='/static/components/Correct.png'><input type='image' class='cancel_img' src='/static/components/Cancel.png' </form>");
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
        $(this).closest('div').find('input[type="text"]').attr('value', comment_value);

        // Cancel X to replace the existing comment data
        $('.cancel_img').on('click', function(){
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
        // console.log($(this).parents().children('.replaced_editor').find('.post_info').text());
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
            // console.log(this);
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
         $('.replacer_editor').on('change','.input_post_file_iedit',function(){
            console.log($(this));
            if(this.files && this.files[0]){
                // console.log($(this).parents('div .row').find('.img_cont'))
                $(this).parents('.re_post').find('.img_cont').attr('src',URL.createObjectURL(this.files[0])).show();
                $(this).parents('.re_post').find('.img_count').onload = function(){
                URL.revokeObjectURL(this.src);
                }
            }

         });
    });
    // Cancelling the edit action of dynamic edit
    $('.replacer_editor').on('click','#cancel_btn', function(){
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
    $('.replacer_editor').on('submit', '.re_post', function(event){
        event.preventDefault();
        var form = $(this)
        var feed_id = $(this).parents('.replacer_editor').attr('id');

        $.ajax({
            url:'edit/'+feed_id+'/',
            context:this,
            type: form.attr('method'),
            data: form.serialize(),
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


// $(function(){

// });