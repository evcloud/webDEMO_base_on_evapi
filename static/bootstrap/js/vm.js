var VM_TASK_CN = {
	'start': gettext('启动'),
	'reboot': gettext('重启'),
	'shutdown': gettext('关闭'),
	'poweroff': gettext('关闭电源'),
	'delete': gettext('删除'),
	'reset': gettext('重置')
}

var VM_STATUS_CN = {
	0: gettext('故障0'), //无状态
	1: gettext('运行'),
	2: gettext('阻塞'),
    3: gettext('暂停'),
    4: gettext('关机'),
    5: gettext('关机'),
    6: gettext('崩溃'),
    7: gettext('暂停'),
    8: gettext('故障1'),  //libvirt预留状态码
    9: gettext('故障2'),  //宿主机连接失败
    10: gettext('故障3')  //虚拟机丢失
}

var VM_STATUS_LABEL = {
		0: 'default',
		1: 'success',
		2: 'info',
	    3: 'info',
	    4: 'info',
	    5: 'info',
	    6: 'danger',
	    7: 'info',
	    8: 'default',
	    9: 'danger',
	    10: 'default'
}

function action(url, vmid, action, success_callback, error_callback, complete_callback) {
	$.ajax({
		url: url,
		type: 'post',
		data: {
			'vmid': vmid,
			'op': action,
		},
		success:success_callback,
		error: error_callback,
		complete:complete_callback
		
	}, 'json');
}

function update_status(url, vmids, interval){
	for(var i in vmids) {
		setInterval("get_status('"+url+"', '" + vmids[i] + "')", interval);
		get_status(url, vmids[i]);
	}
}

function get_status(url, vmid) {
	$.ajax({
		url: url,
		type: 'post',
		data: {
			'vmid': vmid,
		},
		cache:false,
		success: function(data) {
			if (data.res == true){
				$("#" + window.vm_status_tag + data.vmid).html("<span class='label label-" + VM_STATUS_LABEL[data.status] + "'>" + VM_STATUS_CN[data.status] + "</span>");
			}
		},
	}, 'json');
}

function vm_reboot(url, vmid){
	if(!confirm(gettext('确定重启虚拟机？')))
		return;
	$("#" + window.vm_task_tag + vmid).html(VM_TASK_CN["reboot"]);
	action(url, vmid, 'reboot',
		function(data){
			if(data.res) {
				alert(gettext('重启成功')+"！");
			} else {
				alert(gettext('重启失败')+"： " + data.error);
			}
		},
		function(data){},
		function(data){
			get_status(window.vm_status_url , vmid);
			$("#" + window.vm_task_tag + vmid).html("");
		}
		);
}

function vm_shutdown(url, vmid){
	if(!confirm(gettext('确定关闭虚拟机？')))
		return;
	$("#" + window.vm_task_tag + vmid).html(VM_TASK_CN["shutdown"]);
	action(url, vmid, 'shutdown',
		function(data){
			if(data.res) {
			} else {
				alert(gettext('关闭虚拟机失败')+"： " + data.error);
			}
		},
		function(data){},
		function(data){
			get_status(window.vm_status_url , vmid);
			$("#" + window.vm_task_tag + vmid).html("");}
		);
}

function vm_poweroff(url, vmid){
	if(!confirm(gettext('确定强制关闭虚拟机电源？')))
		return;
	$("#" + window.vm_task_tag + vmid).html(VM_TASK_CN["poweroff"]);
	action(url, vmid, 'poweroff',
		function(data){
			if(data.res) {
			} else {
				alert(gettext('关闭电源失败')+"： " + data.error);
			}
		},
		function(data){},
		function(data){
			get_status(window.vm_status_url , vmid);
			$("#" + window.vm_task_tag + vmid).html("");}
		);
}

function vm_start(url, vmid){
	$("#" + window.vm_task_tag + vmid).html(VM_TASK_CN["start"]);
	action(url, vmid, 'start',
		function(data){
			if(data.res) {
			} else {
				alert(gettext('启动失败')+"： " + data.error);
			}
		},
		function(data){},
		function(data){
			get_status(window.vm_status_url , vmid);
			$("#" + window.vm_task_tag + vmid).html("");}
		);
}

function vm_delete(url, vmid){
	if(!confirm(gettext('确定删除虚拟机？')))
		return;
	$("#" + window.vm_task_tag + vmid).html(VM_TASK_CN["delete"]);
	action(url, vmid, 'delete',
		function(data){
			if (data.res == true) {
				$("#tr_" + vmid).remove();
			} else {
				alert(gettext('删除失败')+"： " + res.error);
			}
		},
		function(data){},
		function(data){
			get_status(window.vm_status_url , vmid);
			$("#" + window.vm_task_tag + vmid).html("");}
		);
}

function vm_reset(url, vmid){
	if(!confirm(gettext('确定重置虚拟机？')))
		return;
	$("#" + window.vm_task_tag + vmid).html(VM_TASK_CN["reset"]);
	action(url, vmid, 'reset',
		function(data){
			if(data.res) {
				alert(gettext('重置成功！'));
			} else {
				alert(gettext('重置失败')+"： " + data.error);
			}
		},
		function(data){},
		function(data){
			get_status(window.vm_status_url , vmid);
			$("#" + window.vm_task_tag + vmid).html("");
		}
		);
}