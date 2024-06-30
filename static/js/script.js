$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: 'dd mmm, yyyy', 
        yearRange: 60 
    });
    $('.timepicker').timepicker();
});
