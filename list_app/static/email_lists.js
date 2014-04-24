/**********
 	The EmailLists singleton provides an interface to grab data about all the email lists a user is an administrator of.
**********/
function EmailLists(list_array)
{	
	var lists = list_array;

	function get_list_by_id(id)
	{
		for(i = 0; i < lists.length; i++)
		{
			list = lists[i];
			if(list.id === id)
			{
				return list;
			}
		}

		return null;
	}

	function get_list_by_name(name)
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
}