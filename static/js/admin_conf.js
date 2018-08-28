$(function(){
	$("#id_group_id").after("<img id='id_gropu_id_after' src='/static/images/loading.gif' width='50px'  />")
	$("#id_image_id").after("<img id='id_image_id_after' src='/static/images/loading.gif' width='50px'  />")
	$("#id_image_id_after").hide();
	$.ajax({
		url: '/admin/get_group_list/',
		type: 'get',
		data: {
		},
		success: function (data) {
			var html = '';
			for (var i in data) {
				html += "<option value='" + data[i]['id'] +"'>" + data[i]['name'] + "</option>";
			}
			$("#id_group_id").html(html);
			$("#id_gropu_id_after").hide();
			
			get_image_list(data[0]['id']);
			
		},
		error: function (){}
	}, 'json');
	
	$("#id_group_id").change(function(){
		get_image_list(this.value);
	})
	
})


function get_image_list(group_id) {
	$("#id_image_id_after").show();
	
	$("#id_image_id").html("");
	$.ajax({
		url: '/admin/get_image_list/',
		type: 'get',
		data: {
			'group_id': group_id
		},
		success: function (data) {
			var html = '';
			for (var i in data) {
				html += "<option value='" + data[i]['id'] +"'>" + data[i]['name'] + " " + data[i]['version'] + "</option>";
			}
			$("#id_image_id").html(html);
			$("#id_image_id_after").hide();
					
			
		},
		error: function (){}
	}, 'json');
}
