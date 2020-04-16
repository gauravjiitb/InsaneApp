$(function()
{
    $('.entry').find('.row:not(:last) .btn-add')
                .removeClass('btn-add').addClass('btn-remove')
                .removeClass('btn-success').addClass('btn-danger')
                .html('-');
    var total_forms = parseInt($('#id_form-TOTAL_FORMS').val())
    $(document).on('click','.btn-add', function(e){
        e.preventDefault();
        total_forms +=1;
        $('#id_form-TOTAL_FORMS').val(total_forms)
        var controlForm = $('.entry');
        var currentEntry = $(this).parent();
        var newEntry = $(currentEntry.clone()).appendTo(controlForm);
        newEntry.find('input').val('');
        controlForm.find('.row:not(:last) .btn-add')
                    .removeClass('btn-add').addClass('btn-remove')
                    .removeClass('btn-success').addClass('btn-danger')
                    .html('-');
        controlForm.find(".row:last p:contains(Brand Number) input")
                    .attr("name",('form-'+(total_forms-1)+'-brand_number'))
                    .attr("id",('id_form-'+(total_forms-1)+'-brand_number'));
        controlForm.find(".row:last p:contains(Brand Name) input")
                    .attr("name",('form-'+(total_forms-1)+'-name'))
                    .attr("id",('id_form-'+(total_forms-1)+'-name'));
    }).on('click', '.btn-remove', function(e){
        e.preventDefault();
        total_forms -=1;
        $('#id_form-TOTAL_FORMS').val(total_forms)
        var deleted_row_id = parseInt($(this).parent().find('p:first input').attr("name").split("-")[1]);
        var next_rows = $(this).parent().nextAll();
        next_rows.each(function(){
          row_id = parseInt($(this).find('p:first input').attr("name").split("-")[1]);
          $(this).find("p:contains(Brand Number) input")
                      .attr("name",('form-'+(row_id-1)+'-brand_number'))
                      .attr("id",('id_form-'+(row_id-1)+'-brand_number'));
          $(this).find("p:contains(Brand Name) input")
                      .attr("name",('form-'+(row_id-1)+'-name'))
                      .attr("id",('id_form-'+(row_id-1)+'-name'));
        });
    		$(this).parent().remove();
        console.log($('form').html());
		// return false;
	});
});
