var App = 
    {
        editing_list: false,
        default_text: 'hello world!',
        edit_element: null,
        editing_html: 
            "<textarea name= \"expiration_date\">list expiration date</textarea>",
        normal_html: 
            "<td name= \"expiration_date\">list expiration date</td>",
    };

function on_edit_button_click()
{
    if(App.editing_list)
    {
        list_expire_html = $("tr[name={{listEntry.name}}_row] td[name=exire_date]");
        list_expire_html.replaceWith(App.normal_html);
        $(this).html("edit");
        
        App.editing_list = false;
    }
    else
    {
        list_expire_html = $("tr[name={{listEntry.name}}_row] textarea[name=expire_date]");
        $("td[name=expiration_date]").html(App.editing_html);
        $(this).html("save");
        
        App.editing_list = true;
    }
}

$(document).ready(function()
{
    init();
    $('button').click(on_edit_button_click);
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
