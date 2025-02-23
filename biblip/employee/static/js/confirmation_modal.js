$('.modal-button').click(function(){
    var borrow_id=$(this).attr("borrow_id");
    var modal_type=$(this).attr("modal_type");
    
    
    var modal=document.getElementById('modal-'+modal_type+"-"+borrow_id);
    console.log(modal)
    modal.showModal();

    var close_modal=document.getElementById('close-'+modal_type+"-"+borrow_id);
    close_modal.addEventListener('click',function(){
      modal.close();
    },{once:true});

    var next_button=document.getElementById('next-'+modal_type+'-button'+borrow_id);
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