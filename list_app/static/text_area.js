$("#list_edit_form.value").on('focus', function(){

    console.log("hello world! focus");

    if(this.value == 'default_value')
    {
        this.value = '';
        showCalendarControl(this);
    }
}).on('blur', function(){

    console.log("hello world! blur");

    if( this.value == '')
    {
        this.value = 'default_value';
        hideCalendarControl(this);
    }
})