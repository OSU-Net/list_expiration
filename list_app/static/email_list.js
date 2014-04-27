var EmailList = function(id, name, expire_date)
{
	instance = this;
    list_id = id;
    list_name = name;
    expire_date = expire_date;
    is_editing = false;

    this.get_list_id = function() { return list_id; }
    this.get_list_name = function() { return list_name; }
    this.get_expire_date = function() { return expire_date; }
    this.is_editing = function() { return is_editing; }
}