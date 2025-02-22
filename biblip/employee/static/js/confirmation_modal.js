$('.modal-button').click(function(){
    var borrow_id=$(this).attr("borrow_id");
    
    var modal=document.getElementById('modal-'+borrow_id);
    modal.showModal();


    var close_modal=document.getElementById('close'+borrow_id);
    close_modal.addEventListener('click',function(){
      modal.close();
    },{once:true});

    var next_button=document.getElementById('next-button'+borrow_id);
    next_button.addEventListener('click',function(event){
      event.preventDefault();
      modal.close(); 
      
      var url= $(this).attr('href');
      $.ajax({
        url:url,
        type: "GET",
        success:function(response){
          if (response.success) {

            location.reload();
          } 
        },
        error:function(e){
          console.error('erro',e.responseText)
        }
        
      });
    });
  });