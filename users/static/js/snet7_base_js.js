// Users/base main javascript file

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

// Datepicker Jquery function
$(document).ready(function(){
	$("#datepicker").datepicker({dateFormat: "dd/mm/yy", });
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
	$.each(data, function(index, data){
		// console.log(data)
		var url_val;
		url_val = data.url_val;
		// console.log(url_val);
		if (data.no_result)
		{
			$('#id_search_results').append("<li class='list-group-item'><h6 class='small p-3'>No Results found</h6></li>")
		}
		else{
			// if logged in user and resulted user same
			if(data.fname_empty){
				// If the user firstname is empty
				if(data.friends == 'Friends' || data.friends == 'Request Sent' || data.friends == 'Accept'){
					$('#id_search_results').prepend("<li class='list-group-item'><div class='container'><div class='col-sm-6'><a class='' href='"+url_val+"'><img class='img-thumbnail rounded-circle' width='50' height='50' src='"+data.img_url+"'>"+data.user+"</a></div><div class='col-sm-6'><button type='button' class='freq_sub btn btn-sm btn-info'>"+data.friends+"</button></div></div></li>")
					var val = data.friends;
				}
				else{
					// console.log('first else')
					$('#id_search_results').prepend("<li class='list-group-item'><div class='container'><div class='col-sm-6'><a class='' href='"+url_val+"'><img class='img-thumbnail rounded-circle' width='50' height='50' src='"+data.img_url+"'>"+data.user+"</a></div><div class='col-sm-6'><button type='button' class='freq_sub btn btn-sm btn-info'>"+data.friends+"</button></div></div></li>")
					var val = data.friends;
					}
			}
			// if the logged in user and commenting user are different
			else{
				// console.log("in else")
				if(data.friends == 'Friends' || data.friends == 'Request Sent' || data.friends == 'Accept'){
					$('#id_search_results').prepend("<li class='list-group-item'><div class='container'><div class='col-sm-6'><a class='' href='"+url_val+"'><img class='img-thumbnail rounded-circle' width='50' height='50' src='"+data.img_url+"'>"+data.user+"</a></div><div class='col-sm-6'><button type='button' class='freq_sub btn btn-sm btn-info'>"+data.friends+"</button></div></div></li>")
					var val = data.friends;
				}
				// Updating the Comment Username as per the first_name saved in DB
				else{
					// console.log('second else')
					$('#id_search_results').prepend("<li class='list-group-item'><div class='container'><div class='col-sm-6'><a class='' href='"+url_val+"'><img class='img-thumbnail rounded-circle' width='50' height='50' src='"+data.img_url+"'>"+data.user+"</a></div><div class='col-sm-6'><button type='button' class='freq_sub btn btn-sm btn-info'>"+data.friends+"</button></div></div></li>")
					var val = data.friends;
				}
			}
		}
		// console.log($('.freq_sub').text('Request Sent'));
		console.log(val);
		if(val=='Request Sent'){
			$(".freq_sub:contains('Request Sent')").addClass('btn-primary').removeClass('btn-info');
		}else if(val=='Accept'){
			$(".freq_sub:contains('Accept')").addClass('btn-success').removeClass('btn-info');
		}
	});
}

// Friend Request Sending in the dropdown

$(function(){
	$('#id_search_results').on('click','.freq_sub', function(event){
		event.preventDefault();
		var val = $(this).text();
		// console.log(this);
		// console.log(val);
		if(val=='Send Request'){
			// console.log(this);
			// console.log($(this).parents('div .container').find("a").attr('href'));
			var a_url = $(this).parents('div .container').find("a").attr('href');
			var id = a_url.split('/')[2];
			console.log(id);
			$.ajax({
				url: '/friends_req/'+id+'/',
				context: this,
				type: 'post',
				data: {'freq':'yes'},
				success: function(){
					// console.log('suck');
					$(this).replaceWith('<button class="btn btn-sm btn-primary">Request Sent</button>');
				},

			});
		}
		else if(val=='Accept'){
			var a_url = $(this).parents('div .container').find('a').attr('href');
			var id = a_url.split('/')[2];
			$.ajax({
				url:'/friends_accp/'+id+'/',
				context:this,
				type:'post',
				data:{'friends':'Yes'},
				success:function(){
					$(this).replaceWith('<button class="btn btn-sm btn-success">Friends</button>');
					$('.heart').attr('src', '/static/components/empty_heart.png');
				}
			});
		}
	});
});


// Profile image loading belongs to the Users App

$(document).ready(function(){
	$('#profile_overlay').click(function(){
		$('#inimgF').click();
	});	
});

// Profile image uploading belongs to the Users App

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



// Cover photo change and display belongs to the Users App
$(document).ready(function() {
	$('#cover-chng-btn').click(function(e){
		e.preventDefault();
		$('#cover_photo_file').click();
	});
});

// Cover photo upload to the server belongs to the Users App
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

// Profile data update function belongs to the Users App

$(document).ready(function(){
$('#profile_user_data_form').on('submit', function(e){
	e.preventDefault();
	var form = $('#profile_user_data_form');
	// console.log(form.attr('data-url'));
	// console.log(form.serialize());
	$.ajax({
		url: form.attr('data-url'),
		type: form.attr('method'),
		data: form.serialize(),
		success: function(data){
			$('#prof_sub_btn').blur();
			// console.log('what..?')
			// console.log($('#title').text());
			$('#title').text(data.title)
		}

		});
	});
});


// Friend request form belongs to the Users App

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




// $()



