// Users/base main javascript file

// Datepiceet Jquery function
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
				$(this_c).val("");
				// if logged in user and commenting user same
				if(data.value){
					if(data.fname_empty){
						$(data.id).prepend("<li class='list-group-item p-0'><small><a href='"+url_val+"'>"+data.user+"</a>"+" "+data.comments+"</small></li>")
						// console.log("<li class='list-group-item p-0'><small><a href="+url_val+">"+data.user+"</a>"+data.comments+"</small></li>")
					}
					// Updating the Comment Username as per the first_name saved in DB
					else{
						// console.log('first else')
						$(data.id).prepend("<li class='list-group-item p-0'><small><a href='"+url_val+"''>"+data.user+"</a>"+" "+data.comments+"</small></li>")
					}
				}
				// if the logged in user and commenting user are different
				else{
					// console.log("in else")
					if(data.fname_empty){
						$(data.id).prepend("<li class='list-group-item p-0'><small><a href=/"+url_val+"''>"+ data.user +"</a>"+" "+data.comments+"</small></li>")
					}
					// Updating the Comment Username as per the first_name saved in DB
					else{
						// console.log('second else')
						$(data.id).prepend("<li class='list-group-item p-0'><small><a href='"+url_val+"''>"+ data.user +"</a>"+" "+data.comments+"</small></li>")
					}
				}
			},
		});
	});
});
// This Jquery is meant for the dorpdown show and hide
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

$(document).ready(function(){
	$('.profile-image-container').click(function(){
		$('#inimgF').click();
	});	
});


$('#inimgF').change(function(){
	if(this.files && this.files[0]){
		var reader = FileReader();
		$(reader).load(function(e){
			$('profile_image').attr('src',e.target.result);
		});
		reader.readAsDataURL(this.files[0]);
	}
});

