/**********
 	The EmailLists singleton provides an interface to grab data about all the email lists a user is an administrator of.
**********/
function EmailLists(list_array)
{	
	var that = this;
	var lists = list_array;

	this.get_list_by_id = function(id)
	{
		for(i = 0; i < lists.length; i++)
		{
			list = lists[i];
			if(list.id == id)
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

