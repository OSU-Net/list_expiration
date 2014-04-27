/**********
 	The EmailLists singleton provides an interface to grab data about all the email lists a user is an administrator of.
**********/
function EmailLists(list_array)
{	
	var instance = this;
	var lists = list_array;
	var is_editing = false;

	function get_date_delta(earlier_date, later_date)
	{   
	    return new Date(later_date.getTime() - earlier_date.getTime());
	}

	function validate_list_edit(list_id)
	{
		var new_expire_date_str = $("form[name=edit_form] div[name=expire_date] input[name=expire_date]").val();
		console.log(new_expire_date_str);

	    var new_expire_date = Date(expiration_date_str);
	    var current_expire_date = instance.get_list_by_id(list_id);
	    var delta_years = get_date_delta(current_expire_date,new_expire_date).getYears();

	    if(delta_years >= 2 || delta_years <= 0)
	    {
	        alert("Invalid expiration date!  Choose a date within two years of the current expiration date.");
	        return false;
	    }

	    return true;
	}

	this.get_list_by_id = function(list_id)
	{
		for(i = 0; i < lists.length; i++)
		{
			list = lists[i];
			if(list.id == list_id)
			{
				return list;
			}

			console.log(list.id);
		}

		return null;
	}

	this.get_list_by_name = function(name)
	{
		for(i = 0; i < lists.length; i++)
		{
			list = lists[i];
			if(list.name === name)
			{
				return list;
			}
		}
		
		return null;
	}

	this.get_list_being_edited = function()
	{
		for(i = 0; i < lists.length; i++)
		{
			if(lists[i].is_editing)
			{
				return lists[i];
			}
		}
	}

	this.start_editing = function(list_id)
	{
		if(is_editing)
		{
			return false;
		}

		is_editing = true;
		
		var list = instance.get_list_by_id(list_id)
		if(!list)
		{
			throw "list does not exist!";
		}
		else
		{
			list.is_editing = true;
			return true;
		}
	}

	this.end_editing = function()
	{
		if(!is_editing)
		{
			throw "Not editing a list!";
		}
		else
		{
			is_editing = false;
		}

		for(i = 0; i < lists.length; i++)
		{
			list = lists[i];
			if(list.is_editing)
			{
				if(!validate_list_edit(list.id))
				{
					return false;
				}
				else
				{
					list.is_editing = false;
					return true;
				}
			}
		}
	}

	return this;
}

