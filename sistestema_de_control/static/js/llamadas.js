$("table tr td a").on("click",function(e){
		e.preventDefault()
		var urla=$(this).attr("href");  
		if (urla == '/ok/'){
			var r=$(this).attr("id");
			$.ajax({
				type:'GET',
				url:r,
				beforeSend:Espera,
				success:function(res){
					$('.x_content').html(res);
				}
			});
			function Espera(){
        		$(".x_content").html('<img src="/static/img/log.gif" id="icono"></img><br>Procesando...');
     		}
		}
		else{
			
		}
		
	});