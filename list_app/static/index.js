var App = 
    {
        editing_list: false,
        default_text: 'hello world!',
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

function get_date_delta(earlier_date, later_date)
{   
    return new Date(later_date.getTime() - earlier_date.getTime());
}

function validate_list_edit(list_id, expire_date_str)
{
    var new_expire_date = Date(expiration_date_str);
    var current_expire_date = email_lists.get_list_by_id(list_id);
    var delta_years = get_date_delta(current_expire_date,new_expire_date).getYears();

    if(delta_years >= 2 || delta_years <= 0)
    {
        alert("Invalid expiration date!  Choose a date within two years of the current expiration date.");
        return false;
    }

    return true;
}

function on_edit_button_click()
{
    var id = get_button_list_id(this);
    console.log(id);

    if(App.editing_list)
    {  
        list_expire_html = $("form[name=edit_form]"));

        var list_expire_date = email_lists.get_list_by_id(id).expire_date;
        var normal_html = 
            "<div name=\"expire_date\" class=\"list_field\"> \
                <p><b>List Expiration Date:</b></p>          \
                <p>".concat(list_expire_date).concat("</p>   \
            </div>");
        list_expire_html.replaceWith(normal_html);
        $(this).html("Edit");


        App.editing_list = false;
    }
    else
    {
        list_expire_html = $("div[id=".concat(id).concat("] div[name=expire_date]"));
        
        var editing_html =  
        "<form name=\"edit_form\" action = \"lists\\submit_list_edit\">   
            <div name=\"expire_date\" class=\"list_field\">                                                            \
                <b>List Expiration Date:</b><br>                                                                       \
                <input type=\"text\" name=\"expire_date\" class=\"text_edit_field\"> Choose an expiration date</input> \                                             \
            </div>                                                                                                     \
        </form>";
        list_expire_html.replaceWith(editing_html);

        $("input[name=expire_date]").on('focus', on_text_area_gain_focus).on('blur', on_text_area_lose_focus);

        $(this).html("Save");
        
        App.editing_list = true;
    }
}

$(document).ready(function()
{
    init();
    $(':button').click(on_edit_button_click);
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
