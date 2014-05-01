var EmailList = function(id, name, expire_date)
{
    this.list_id = id;
    this.list_name = name;
    this.expire_date = expire_date;
    this.is_editing = false;
}

EmailList.prototype = 
{
	get_list_id : function() { return this.list_id; },
    get_list_name : function() { return this.list_name; },
    get_expire_date_str : function() { return this.expire_date; },
    is_editing : function() { return this.is_editing; }

    copy : function()
    {
    	return new EmailList(this.id, this.list_name, this.expire_date);
    }
};