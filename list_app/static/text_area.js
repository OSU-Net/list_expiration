$('#expire_date').focusin(function(){
	asdfasdf
	if(this.value == '0')
	{
		this.value = '';
		showCalendarControl(this);
	}
}).focusout(function(){
	if( this.value == '')
	{
		this.value = '0';
		hideCalendarControl(this);
	}
})