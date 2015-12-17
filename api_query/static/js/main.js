jQuery(document).ready(function($){
	//open the lateral panel
	$('.cd-btnb1').on('click', function(event){
		event.preventDefault();
		$('.cd-panelb1').addClass('is-visible');
	});
	//open the lateral panel
	$('.cd-btnb2').on('click', function(event){
		event.preventDefault();
		$('.cd-panelb2').addClass('is-visible');
	});
		//open the lateral panel
	$('.cd-btnb3').on('click', function(event){
		event.preventDefault();
		$('.cd-panelb3').addClass('is-visible');
	});
		//open the lateral panel
	$('.cd-btnb4').on('click', function(event){
		event.preventDefault();
		$('.cd-panelb4').addClass('is-visible');
	});
		//open the lateral panel
	$('.cd-btnb5').on('click', function(event){
		event.preventDefault();
		$('.cd-panelb5').addClass('is-visible');
	});
		//open the lateral panel
	$('.cd-btnr1').on('click', function(event){
		event.preventDefault();
		$('.cd-panelr1').addClass('is-visible');
	});
		//open the lateral panel
	$('.cd-btnr2').on('click', function(event){
		event.preventDefault();
		$('.cd-panelr2').addClass('is-visible');
	});
		//open the lateral panel
	$('.cd-btnr3').on('click', function(event){
		event.preventDefault();
		$('.cd-panelr3').addClass('is-visible');
	});
		//open the lateral panel
	$('.cd-btnr4').on('click', function(event){
		event.preventDefault();
		$('.cd-panelr4').addClass('is-visible');
	});
		//open the lateral panel
	$('.cd-btnr5').on('click', function(event){
		event.preventDefault();
		$('.cd-panelr5').addClass('is-visible');
	});
	
	//clode the lateral panel
	$('.cd-panel').on('click', function(event){
		if( $(event.target).is('.cd-panel') || $(event.target).is('.cd-panel-close') ) { 
			$('.cd-panel').removeClass('is-visible');
			event.preventDefault();
		}
	});
});