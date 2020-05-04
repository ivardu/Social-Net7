// Users/base main javascript file



// Datepicker Jquery function
$(document).ready(function(){
	$("#datepicker").datepicker({dateFormat: "dd/mm/yy", });
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
						$(data.id).prepend("<li class='list-group-item p-0'><div class='d-flex flex-row'><div><a class='small' href='"+url_val+"'>"+data.user+"</a><small>"+" "+data.comments+"</small> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></div></li>")
						// console.log("<li class='list-group-item p-0'><small><a href="+url_val+">"+data.user+"</a>"+data.comments+"</small></li>")
					}
					// Updating the Comment Username as per the first_name saved in DB
					else{
						// console.log('first else')
						$(data.id).prepend("<li class='list-group-item p-0'><div class='d-flex flex-row'><div><a class='small' href='"+url_val+"'>"+data.user+"</a><small>"+" "+data.comments+"</small> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></div></li>")
					}
				}
				// if the logged in user and commenting user are different
				else{
					// console.log("in else")
					if(data.fname_empty){
						$(data.id).prepend("<li class='list-group-item p-0'><div class='d-flex flex-row'><div><a class='small' href='"+url_val+"'>"+data.user+"</a><small>"+" "+data.comments+"</small> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></div></li>")
					}
					// Updating the Comment Username as per the first_name saved in DB
					else{
						// console.log('second else')
						$(data.id).prepend("<li class='list-group-item p-0'><div class='d-flex flex-row'><div><a class='small' href='"+url_val+"'>"+data.user+"</a><small>"+" "+data.comments+"</small> <input class='edit_button' src='/static/components/edit_comment.png/' type='image'></div></div></li>")
					}
				}
			},
		});
	});
});

// Search Dorp-down This Jquery is meant for the dorpdown show and hide
$(document).ready(function(){
	// Clicking in the input text box enables the dropdown div
	$('#nav_search').on('click', function(){
		// console.log('Adam is here..!!')
		var $div_overlay = $('#overlay');
		$('#nav_search').append($div_overlay);
		// $('#overlay').append('<h1 class="text-primary">Testing text</h1>');
		$('#overlay').show();

	});
	// Clicking outside of the dropdown div will hide it
	}).mouseup(function(e){
		var container = $('#overlay');
		var nav_search = $('#ip_nav_search');

		if(!container.is(e.target) && !nav_search.is(e.target) && container.has(e.target).length === 0){	
			$('#id_search_results li').remove();
			container.hide(); 
	}
});

	// AJax Search call for results display in the dropdown div
	$(document).ready(function(){
		$('#ip_nav_search').on('keyup', function(e){
			e.preventDefault();
			var search = $('#ip_nav_search').val(); 
			if(search == ' '){
				$('#id_search_results').append("<li class='list-group-item'><h6 class='small p-3'>No Results found</h6></li>");
			}
			else{
				// Ajax call to the django server for search results
				$.ajax({
					url: $('#search_form').attr('data_url'),
					cache: false,
					type: $('#search_form').attr('method'),
					data: $('#search_form').serialize(),
					success: results,
					error: function(e)
					{
						console.log('am I failing..?');
					}
				});
			}
		}).keyup(function(e){
			if(e.keyCode == 8 || e.keycode == 46){
				$('#id_search_results li').remove();
			}
		});
	});
	function results(data)
	{
		// console.log("What is my status");
		$('#id_search_results li').remove();
		$.each(data, function(index, data)
		{
			// console.log(data)
			var url_val;
			url_val = data.url_val;
			// console.log(url_val);
			if (data.no_result)
			{
				$('#id_search_results').append("<li class='list-group-item'><h6 class='small p-3'>No Results found</h6></li>")
			}
			else{
				// if logged in user and commenting user same
				if(data.value){
					if(data.fname_empty){
						$('#id_search_results').prepend("<li class='list-group-item'><div class='container'><div class='col-sm-6'><a class='' href='"+url_val+"'><img class='img-thumbnail rounded-circle' width='50' height='50' src='"+data.img_url+"'>"+data.user+"</a></div><div class='col-sm-6'><span class='btn btn-sm btn-info'>"+data.friends+"</span></div></div></li>")
					}
					else{
						// console.log('first else')
						$('#id_search_results').prepend("<li class='list-group-item'><div class='container'><div class='col-sm-6'><a class='' href='"+url_val+"'><img class='img-thumbnail rounded-circle' width='50' height='50' src='"+data.img_url+"'>"+data.user+"</a></div><div class='col-sm-6'><span class='btn btn-sm btn-info'>"+data.friends+"</span></div></div></li>")
						}
				}
				// if the logged in user and commenting user are different
				else{
					// console.log("in else")
					if(data.fname_empty){
						$('#id_search_results').prepend("<li class='list-group-item'><div class='container'><div class='col-sm-6'><a class='' href='"+url_val+"'><img class='img-thumbnail rounded-circle' width='50' height='50' src='"+data.img_url+"'>"+data.user+"</a></div><div class='col-sm-6'><span class='btn btn-sm btn-info'>"+data.friends+"</span></div></div></li>")
					}
					// Updating the Comment Username as per the first_name saved in DB
					else{
						// console.log('second else')
						$('#id_search_results').prepend("<li class='list-group-item'><div class='container'><div class='col-sm-6'><a class='' href='"+url_val+"'><img class='img-thumbnail rounded-circle' width='50' height='50' src='"+data.img_url+"'>"+data.user+"</a></div><div class='col-sm-6'><span class='btn btn-sm btn-info'>"+data.friends+"</span></div></div></li>")
					}
				}
			}
	});
}

// Profile image loading

$(document).ready(function(){
	$('#profile_overlay').click(function(){
		$('#inimgF').click();
	});	
});

// Profile image uploading 

$(document).ready(function(){
	$('#inimgF').change(function(){
		if(this.files && this.files[0]){
			// var reader = FileReader();
			// $(reader).load(function(e){
			// 	$('#profile_image').attr('src',e.target.result);
			// });
			// reader.readAsDataURL(this.files[0]);
			$('#profile_image').attr('src',URL.createObjectURL(this.files[0]));
			$('#profile_image').onload = function(){
				URL.revokeObjectURL(this.src);
			}
		}
		var form = new FormData($('#profile_user_form')[0])
		$.ajax({
			url:'/profile/',
			type:$('#profile_user_form').attr('method'),
			data:form,
			processData: false,
			contentType: false,
			beforeSend: function(){$('#loader_gif').show();},
			complete: function(){$('#loader_gif').hide();},
			success: function(data){
				// $('#prof_sub_btn').blur();
				console.log(data);
			},
			error: function(e){
				console.log(e);
			}
		});
	});
});



// Cover photo change and display
$(document).ready(function() {
	$('#cover-chng-btn').click(function(e){
		e.preventDefault();
		$('#cover_photo_file').click();
	});
});

// Cover photo upload to the server
$(document).ready(function(){
	// console.log('what about here');
	$('#cover_photo_file').change(function(){
		// console.log('change is working');
		if(this.files && this.files[0]){
			// var new_reader = new FileReader();
			// $(new_reader).load(function(e){
			// 	$('#cover_photo_img').attr('src', e.target.result);
			// });
			// new_reader.readAsDataURL(this.files[0]);
			// console.log('what about here');
			$('#cover_photo_img').attr('src', URL.createObjectURL(this.files[0])).width('820px').height('462px');
			$('#cover_photo_img').onload = function(){
				// $(this).css('height','820px');
				// $(this).css('width','400px');
				URL.revokeObjectURL(this.src);
			}
		}
		// console.log($('.cover_pic_form')[0]);
		var form = new FormData($('.cover_pic_form')[0]);
		// console.log(form);
		$.ajax({
			url:$('.cover_pic_form').attr('action'),
			type:$('.cover_pic_form').attr('method'),
			data:form,
			processData: false,
			contentType: false,
			beforeSend: function(){$('#cover_loader').show();},
			complete: function(){$('#cover_loader').hide();},
			success: function() {
				$('#cover-chng-btn').blur();
			},

		});
	});
});

// // Cover photo re-size which is not working properly 
// $('#cover_photo_img').load(function(e){
// 	$(this).css({'height':'820px', 'width':'400px'}).show();
// 	// $(this).css('width','400').show();
// })


$(document).ready(function(){
$('#profile_user_data_form').on('submit', function(e){
	e.preventDefault();
	var form = $('#profile_user_data_form');
	console.log(form.attr('data-url'));
	console.log(form.serialize());
	$.ajax({
		url: form.attr('data-url'),
		type: form.attr('method'),
		data: form.serialize(),
		success: function(){
			$('#prof_sub_btn').blur();
		}

		});
	});
});


// Friend request form

$(document).ready(function(){
	$("#friend_req_form").on('submit', function(event){
		event.preventDefault();
		var form = $('#friend_req_form');
		console.log(form);
		$.ajax({
			url: form.attr('action'),
			type: form.attr('method'),
			data: form.serialize(),
			success: function(data){
				$('#friend_req_btn').html('Request Sent');
				$('#friend_req_btn').attr('class', 'btn btn-primary');
			},
		});
	});
});


// Editing the comment section

// Clicking on the Edit button of comment
$(document).ready(function(){
	$('.edit_button').on('click', function(){
		var comment_value = $(this).parent().children('span').text();
		// console.log(comment_value);
		$(this).parent().children('span').replaceWith("<form class='comm-update-form' class='p-1' method='post'><input id='comment_ip' name='comments' class='form-control-sm' type='text'><input class='correct_img' type='image' src='/static/components/Correct.png'><input class='cancel_img' id='cncl_gim' type='image' src='/static/components/Cancel.png'></form>");
		$('.correct_img').css({
				'width': '30px',
				'height':'30px'
		});
		$('.cancel_img').css({
				'width': '30px',
				'height':'30px'
		});
		var edit_ = $(this);
		edit_.hide();
		$(this).closest('div').find('input[type="text"]').attr('value', comment_value);
		// console.log($(this).closest('div').find('li').attr('id'))
		// console.log($(this).closest('#comment_ip').attr('value', comment_value));
		$('.cancel_img').on('click', function(){
			$(this).closest('.comm-update-form').after("<input class='edit_button' src='/static/components/edit_comment.png/' type='image' name='Edit'>").replaceWith('<span class="small">'+comment_value+'</span>');
			// edit_.show();
		});

		// Comment Form Update
		$('.comm-update-form').on('submit', function(e){
		// 	console.log('Why you are not working');
			e.preventDefault();
			var ider = $(this).closest('li').attr('id');
			var comment_form = $('.comm-update-form', this);
			// console.log('/comment_update/'+ider);
			// console.log($('.comm-update-form').attr('method'));
				$.ajax({
					context: this,
					url: 'comment_update/'+ider,
					type: $('.comm-update-form').attr('method'),
					data:{
						// 'csrfmiddlewaretoken': token,
						'comments': $('#comment_ip').val(), 
					},
					success: function(data){
						// console.log();
						$(this).replaceWith('<span class="small">'+data.comment_val+'</span>');
						edit_.show();

					}
				});

		});
	});
});



// $(document).ready(function(){
// 	// var token = $('input[name="csrfmiddlewaretoken"]').val();

// 		$('#comment_ip').on('keyup', function(e){
// 		// 		console.log('Why you are not working');
// 		// e.preventDefault();
// 		console.log('coming here..?');
// 		var ider = $(this).closest('li').attr('id');
// 		var comment_form = $('.comm-update-form', this);
		
// 		console.log('/comment_update/'+ider);

		
// 	});
// });


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