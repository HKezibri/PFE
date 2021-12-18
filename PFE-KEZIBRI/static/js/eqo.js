$(document).ready(function(){
    var dataTable = $('#sample_data').DataTable();
    $('#sample_data').editable({
        container:'body',
        selector:'',
        url:'',
        title:'',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });

 
 
    
}); 
function del(ID, title){
    if (confirm("Are you sure you want to delete '" + title + "'")){
        window.location.href = '/admin/delete-mbr' + ID;
    }
}


