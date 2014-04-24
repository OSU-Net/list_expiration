var App = 
    {
        editing_list: false,
        default_text: 'hello world!',
        edit_element: null,
        editing_html: 
            "<textarea name=\"expire_date\" class=\"list_field\"> \
                list expiration date                              \
            </textarea>", 
        normal_html: 
<<<<<<< HEAD
            "<div name=\"expire_date\" class=\"list_field\"> \
                <p><b>List Expiration Date:</b></p>          \
                <p>{{listEntry.expire_date}}</p>             \
            </div>",
=======
            "<td name= \"expiration_date\">list expiration date</td>",
        list_ids:
>>>>>>> d6f3574614d18c0e48467e5349f16ffbdb9c7f43
    };

function get_button_list_id(button)
{
    var id_str = button.id;
    return id_str.split("_")[2];
}

function on_edit_button_click()
{
    var id = get_button_list_id(this);
    console.log(id);

    if(App.editing_list)
    {  
        list_expire_html = $("div[id=".concat(id).concat("] textarea[name=expire_date]");
        console.log(lookup_str);
        console.log($(lookup_str).length);

        var list_expire_date = email_lists.get_list_by_id(id).expire_date;
        var normal_html = 
            "<div name=\"expire_date\" class=\"list_field\"> \
                <p><b>List Expiration Date:</b></p>          \
                <p>".concat(list_expire_date).concat("</p>             \
            </div>");
        list_expire_html.replaceWith(normal_html);
        $(this).html("Edit");
        
        App.editing_list = false;
    }
    else
    {
        limvst_expire_html = $("div[id=".concat(id).concat("] div[name=expire_date]");
        console.log(lookup_str);
        console.log($(lookup_str).length);
        
        var editing_html =  
            "<textarea name=\"expire_date\" class=\"list_field\"> \
                list expiration date                                             \
            </textarea>";
        list_expire_html.replaceWith(editing_html);

        $(this).html("Save");
        
        App.editing_list = true;
    }
}

$(document).ready(function()
{
    init();
<<<<<<< HEAD
    $(':button').click(on_edit_button_click);
=======
    buttons = $('[name^=edit_button]').click(on_edit_button_click);
    for(var i=0; i < buttons.length(); i++)
    {
        var strings = buttons[i].split("_");
        var list_id = strings[strings.length-1];
    }
>>>>>>> d6f3574614d18c0e48467e5349f16ffbdb9c7f43
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
