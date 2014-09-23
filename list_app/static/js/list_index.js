
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

function on_date_field_gain_focus(id)
{
    var element = $("form[id=edit_form_".concat(id).concat("] input[name=expire_date]"));
    element.css("color", "#000000");
    var list = email_lists.get_list_by_id(id);
    
    element.val("");
    //element.val(list.get_expire_date_str());
}

function on_date_field_lose_focus(id)
{
    var element = $("form[id=edit_form_".concat(id).concat("] input[name=expire_date]"));
    element.css("color", "#AAAAAA"); 
    element.val(list.get_expire_date_str());   
}

function on_date_selected(text, obj)
{
    id = email_lists.get_list_being_edited().get_list_id();
    $("form[id=edit_form_".concat(id).concat("] input[name=expire_date]")).css("color", "#000000");        
}

function cancel_editing(id)
{
    //show expire_date div
    $("tr[id=".concat(id).concat("]").concat(" p ")).show();

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
    //$("div[id=expire_date_".concat(id).concat("]")).hide();
    $("td[id=expire_date_".concat(id).concat("] p")).hide();    
    
    //show editable expire_date text field
    $("form[id=edit_form_".concat(id).concat("] input[type=text]")).show();

    //change 'edit' button to 'save'
    $("button[id=edit_button_".concat(id).concat("]")).html('Save');

    //make 'cancel' and forward buttons visible
    $("button[id=cancel_button_".concat(id).concat("]")).show();
    $("button[id=forward_button_".concat(id).concat("]")).show();

    var date_field = $("form[id=edit_form_".concat(id).concat("] input[type=text]"));
    var default_date = email_lists.get_list_by_id(id).get_expire_date_str();
    
    //date_field.datepicker({ dateFormat: "yy-mm-dd"})
    //date_field.datepicker("option", "defaultDate", default_date);
    date_field.datepicker({ 
        dateFormat: "yy-mm-dd",
        defaultDate: default_date,
        onSelect: on_date_selected 
    });
    //date_field.datepicker();

    date_field.blur(function()
    {
        on_date_field_lose_focus(id);
    });

    date_field.focus(function()
    {
        on_date_field_gain_focus(id);
    });
    
    on_date_field_lose_focus(id); // call this to make 'ghost' text appear
    email_lists.start_editing(id);
}

//stops editing list with id 'id'
function end_editing(id)
{
    email_lists.end_editing();

    $("td[id=expire_date_".concat(id).concat("]")).show();

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
	var forward_date = new Date(date.getFullYear() + 2, date.getMonth(), date.getDate());
    return String(forward_date.getFullYear()).concat("-").concat(String(forward_date.getMonth())).concat("-").concat(String(forward_date.getDate()));
}

function on_forward_button_click()
{
    var id = get_element_list_id(this);
	var list = email_lists.get_list_by_id(id);

	var expire_date = calc_2_years_forward(new Date());
    //break the string apart and correct the month because Date() assumes [0-11] months and I want [1-12]
    var date_elements = expire_date.split("-");	
    var new_month = parseInt(date_elements[1]) + 1;
    var new_date_str = date_elements[0].concat("-").concat(new_month).concat("-").concat(date_elements[2]);
    $("form[id=edit_form_".concat(id).concat("] input[type=text]")).val(new_date_str);
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
