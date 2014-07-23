
var text_area_stored_text = null;

function get_element_list_id(element)
{
    var id_str = element.id;
    var id_strs = id_str.split("_");
    return id_strs[id_strs.length - 1];
}

function on_cancel_button_click()
{
    var id = get_element_list_id(this);
    cancel_editing(id);
}

function cancel_editing(id)
{
    //show expire_date div
    $("div[id=expire_date_".concat(id).concat("]")).show();

    //hide editable expire_date text field
    $("form[id=edit_form_".concat(id).concat("] input[type=text]")).val("");
    $("form[id=edit_form_".concat(id).concat("] input[type=text]")).hide();

    //change 'save' button to edit
    $("button[id=edit_button_".concat(id).concat("]")).html('Edit');

    //hide 'cancel' and 'forward' buttons
    $("button[id=cancel_button_".concat(id).concat("]")).hide();
    $("button[id=forward_button_".concat(id).concat("]")).hide();
    
    email_lists.cancel_editing();
}

//Performs two functions: modifies list index page visually to open editing options.  Also signals to 'email_lists'
//to begin editing on list with id 'id'
function begin_editing(id)
{
    //hide readonly expire_date div
    $("div[id=expire_date_".concat(id).concat("]")).hide();

    //show editable expire_date text field
    $("form[id=edit_form_".concat(id).concat("] input[type=text]")).show();

    //change 'edit' button to 'save'
    $("button[id=edit_button_".concat(id).concat("]")).html('Save');

    //make 'cancel' and forward buttons visible
    $("button[id=cancel_button_".concat(id).concat("]")).show();
    $("button[id=forward_button_".concat(id).concat("]")).show();

    var date_field = $("form[id=edit_form_".concat(id).concat("] input[type=text]"));
    var default_date = email_lists.get_list_by_id(id).get_expire_date_str();
    
    date_field.datepicker({ dateFormat: "yy-mm-dd"})
    date_field.datepicker("option", "defaultDate", default_date);
    date_field.datepicker();

    email_lists.start_editing(id);
}

//stops editing list with id 'id'
function end_editing(id)
{
    email_lists.end_editing();

    //show expire_date div
    $("div[id=expire_date_".concat(id).concat("]")).show();

    //hide editable expire_date text field
    $("form[id=edit_form_".concat(id).concat("] input[type=text]")).hide();

    //change 'save' button to edit
    $("button[id=edit_button_".concat(id).concat("]")).html('Edit');

    //hide 'cancel' and 'forward' buttons
    $("button[id=cancel_button_".concat(id).concat("]")).hide();
    $("button[id=forward_button_".concat(id).concat("]")).hide();
}

//return a Date string with format "YYYY-MM-DD" that is set out two years from 'date'
function calc_2_years_forward(date)
{
	var forward_date = new Date(date.getFullYear() + 2, date.getMonth(), date.getDay());
    return String(forward_date.getFullYear()).concat("-").concat(String(forward_date.getMonth())).concat("-").concat(String(forward_date.getDate()));
}

function on_forward_button_click()
{
    var id = get_element_list_id(this);
	var list = email_lists.get_list_by_id(id);

	var expire_date = calc_2_years_forward(new Date());

	$("form[id=edit_form_".concat(id).concat("] input[type=text]")).val(expire_date);
}

function on_edit_button_click()
{
    var id = get_element_list_id(this);
    var list = email_lists.get_list_being_edited();
    
    if(list == null)
    {  
        begin_editing(id);
        var i = 0;
    }
    else
    {
        if(list.get_list_id() != id)
        {
            alert("You can only edit one list at a time.")
            return; //can't edit two lists at once!
        }

        end_editing(id);
    }
}

$(document).ready(function()
{
    $('button[name=edit_button]').click(on_edit_button_click);
    $('button[name=cancel_button]').click(on_cancel_button_click);
    $('button[name=forward_button]').click(on_forward_button_click);

    $("form[name=edit_form] input[type=text]").hide();
    $("button[name=cancel_button]").hide();
    $("button[name=forward_button]").hide();
});