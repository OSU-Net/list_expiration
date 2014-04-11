$("#list_edit_form input[name='expire_date']").on('focus', function(){

    console.log("hello world! focus");

    if(this.value == window.$vars.default_text)
    {
        this.value = '';
        showCalendarControl(this);
    }
}).on('blur', function(){

    console.log("hello world! blur");

    if( this.value == '')
    {
        this.value = window.$vars.default_text;
        hideCalendarControl(this);
    }
})