
document.addEventListener("DOMContentLoaded", function() {
	var msgForm = document.getElementById("my-message-form-id");
	console.log("msgForm is",msgForm);
	msgForm.onkeydown = function(){
		console.log("typing now");
		msgForm.style.position = 'absolute';
		msgForm.style.bottom = '170px';
		//msgForm.style.left = '100px';
		msgForm.style.width = "100%";
	}

	//var msgForm = document.getElementById("my-message-form-id");
	msgFormInput = document.querySelector(".ql-editor");
	//var mfi = msgFormInput[0];
	console.log(msgFormInput); //console.log(mfi);
	msgFormInput.addEventListener("blur", function(){
		console.log("not typing");
		msgForm.style.position = 'absolute';
		msgForm.style.bottom = '0px';
		//msgForm.style.left = '100px';
		msgForm.style.width = "100%";
	});
});
