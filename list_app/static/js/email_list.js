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
    is_editing : function() { return this.is_editing; },

    get_expire_date_obj : function() 
    {  
        var date_strs = this.expire_date.split("-");
        var date_obj = new Date(date_strs[0], date_strs[1], date_strs[2], 0, 0, 0);
        return date_obj;
    },

    clone : function()
    {
    	return new EmailList(this.id, this.list_name, this.expire_date);
    }
};