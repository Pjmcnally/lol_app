jQuery(document).ready(function($){
	//open the lateral panel
	$('.cd-btn').on('click', function(event){
		event.preventDefault();
		var parId = $(event.target).parent().attr("id");
		$("."+parId).addClass('is-visible');
	});	
	
	//clode the lateral panel
	$('.cd-panel').on('click', function(event){
		if( $(event.target).is('.cd-panel') || $(event.target).is('.cd-panel-close') ) { 
			$('.cd-panel').removeClass('is-visible');
			event.preventDefault();
		}
	});
	var clock = document.getElementById("clock");
	var time = document.getElementById("clockVar").value;
	setInterval(function() {
		time ++;
		if (time <= 0) {
			clock.innerHTML = "Loading"
		} else {
			seconds = Math.floor(time % 60);
			minutes = Math.floor((time/60) % 60);
			hours = Math.floor(time/3600);
			clock.innerHTML = ": " +  hours + ":" + checkNum(minutes) + ":" + 
			    checkNum(seconds);
		} 	
	}, 1000);
	function checkNum(num) {
		if (num < 10) {
			return "0" + num;
		} else {
			return num;
		}
	}
	
});