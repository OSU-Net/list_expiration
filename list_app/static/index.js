var App = 
{
    edit_element: null,
};

var text_area_stored_text = null;

function get_button_list_id(button)
{
    var id_str = button.id;
    return id_str.split("_")[2];
}

function on_text_area_gain_focus(text_area)
{
    console.log("on_focus");

    text_area_stored_text = text_area.value;
    text_area.value = '';
    showCalendarControl(this);
}

function on_text_area_lose_focus(text_area)
{
    console.log("on_blur");
    if( this.value == '')
    {
        this.value = App.default_text;
        hideCalendarControl(this);
    }
}

function on_cancel_button_click()
{
    var id = get_button_list_id(this);
    end_editing(id);
}

//Performs two functions: modifies list index page visually to open editing options.  Also signals to 'email_lists'
//to begin editing on list with id 'id'
function begin_editing(id)
{
    list_expire_html = $("div[id=".concat(id).concat("] div[name=expire_date]"));
    
    //add in a text field to allow modification of the expiration date
    var editing_html =  
    "<form name=\"edit_form\" action = \"lists\\submit_list_edit\" method=\"post\">                                   \
        <div name=\"expire_date\" class=\"list_field\">                                                               \
            <b>List Expiration Date:</b><br>                                                                          \
            <input type=\"text\" name=\"expire_date\" class=\"text_edit_field\" value=\"choose an expiration date\">  \                                             \
        </div>                                                                                                        \
        <input type=\"hidden\" name=\"list_id\" value=\"".concat(id).concat("\" />                                    \                                                                                                               \
    </form>");
    list_expire_html.replaceWith(editing_html);

    $("input[name=expire_date]").on('focus', on_text_area_gain_focus).on('blur', on_text_area_lose_focus);

    //change the button text to 'save' and add a cancel button 
    var button = $("button[id=edit_button_".concat(id).concat("]"));
    button.html("Save");
    button.after("<button name=\"cancel_button\" id=\"cancel_button_".concat(id).concat("\" \
                  class=\"cancel_button\" name=\"cancel\"> cancel </button>"));
    
    $("button[name=cancel_button]").click(on_cancel_button_click);
    email_lists.start_editing(id);
}

//stops editing list with id 'id'
function end_editing(id)
{
    email_lists.end_editing();

    list_expire_html = $("form[name=edit_form]");

    //change the edit text area back into a readonly div
    var list_expire_date = email_lists.get_list_by_id(id).expire_date;
    var normal_html = 
        "<div name=\"expire_date\" class=\"list_field\"> \
            <p><b>List Expiration Date:</b></p>          \
            <p>".concat(list_expire_date).concat("</p>   \
        </div>");
    list_expire_html.replaceWith(normal_html);

    //Change 'Save' button back to 'Edit' and remove the cancel button 
    var save_button = $(":button[name=edit_button]");
    save_button.html("Edit");

    $("button[id=\"cancel_button_".concat(id).concat("\"]")).remove();
}

function on_edit_button_click()
{
    var id = get_button_list_id(this);
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
    init();
    $(':button[name=edit_button]').click(on_edit_button_click);
    //$(':button[name=cancel_button]').click(on_cancel_button_click);
});

function init()
{
    App.edit_element = $("td[name=expiration_date]");
    console.log(App.edit_element);
}

function onListEdit()
{
    if(App.editing_list)
    {
        return;
    }
    
    $("textarea[name='edit_text']").on('focus', function(){

        console.log("on_focus");
        if(this.value == App.default_text)
        {
            this.value = '';
            //showCalendarControl(this);
        }

    }).on('blur', function(){

        console.log("on_blur");
        if( this.value == '')
        {
            this.value = App.default_text;
            //hideCalendarControl(this);
        }
    })
}
