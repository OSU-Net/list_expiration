/**********
 	The EmailLists singleton provides an interface to grab data about all the email lists a user is an administrator of.
**********/
function EmailLists(list_array)
{	
	var that = this;
	var lists = list_array;
	var is_editing = false;

	this.get_list_being_edited = function()
	{
		for(i = 0; i < lists.length; i++)
		{
			if(lists[i].is_editing)
			{
				return true;
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
		
		var list = get_list_by_id(list_id)
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
				list.is_editing = false;
				return;
			}
		}
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

	return this;
}

