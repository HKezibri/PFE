$(document).ready(function(){
    var dataTable = $('#sample_data').DataTable();
    $('#sample_data').editable({
        container:'body',
        selector:'td.titre',
        url:'/admin/updateevents',
        title:'Titre',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });
 
    $('#sample_data').editable({
        container:'body',
        selector:'td.categorie',
        url:'/admin/updateevents',
        title:'categorie',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });
    $('#sample_data').editable({
        container:'body',
        selector:'td.courte_description',
        url:'/admin/updateevents',
        title:'courte_description',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });
    $('#sample_data').editable({
        container:'body',
        selector:'td.date_fin',
        url:'/admin/updateevents',
        title:'description',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });
    $('#sample_data').editable({
        container:'body',
        selector:'td.lieu',
        url:'/admin/updateevents',
        title:'lieu',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    });
    $('#sample_data').editable({
        container:'body',
        selector:'td.date_debut',
        url:'/admin/updateevents',
        title:'date_debut',
        type:'POST',
        validate:function(value){
            if($.trim(value) == '')
            {
                return 'This field is required';
            }
        }
    }); 
    $('#sample_data').editable({
        container:'body',
        selector:'td.date_fin',
        url:'/admin/updateevents',
        title:'date_fin',
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
        window.location.href = '/admin/delete-event/' + ID;
    }
}






$(document).ready(function() {
    $('#summernote').summernote();
});