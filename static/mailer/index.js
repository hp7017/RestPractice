$("#show_users").click(function(){
	formData = new FormData($('#mail_form')[0]);
	formData.append('show_users', true)
	console.log('show_users')
	$.ajax({
		type: 'post',
		url: '',
		data: formData,
		processData: false,
		contentType: false,
		enctype: 'multipart/form-data',
		success: function(data){
			if (data.errors) {
				for (name in data.errors) {
					for (i in data.errors[name]){
						$('#mail_form').prepend('<div role="alert" class="alert alert-danger text-left"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><span class="text-right"><strong>' + name + ' : ' + data.errors[name][i].message + '</strong></span></div>')
					}
				}
			}
			else {
				for (i in data.emails){
					$('#email_list').append('<li class="list-group-item">' + data.emails[i] + '</li>')
				}
				$('#email_count').text('Count : ' + data.emails_count)
				$('#html_message').html(data.html_message)
			}
		}
	})
})
$('#mail_form').submit(function(){
	formData = new FormData($('#mail_form')[0])
	formData.append('send_email', true)
	event.preventDefault()
	$.ajax({
		url: '',
		type: 'post',
		data: formData,
		contentType: false,
		processData: false,
		enctype: 'multipart/form-data',
		success: function(data){
			if (data.errors) {
				for (name in data.errors){
					for (i in data.errors[name]){
						$('#mail_form').prepend('<div role="alert" class="alert alert-danger text-left"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><span class="text-right"><strong>' + name + ' : ' + data.errors[name][i].message + '</strong></span></div>')
					}
				}
			}
			else {
				$('#mail_form').prepend('<div role="alert" class="alert alert-success text-left"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><span style="font-size: 20px;">😀<strong> Email has been sent.</strong><br /></span></div>')
			}
		}
	})
})
$('#logout').click(function(){
	$.ajax({
		url: '',
		type: 'post',
		data: {
			'log_out': true,
			'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
		},
		success: function(data){
			window.location.href = data.redirect_page
		}
	})
})