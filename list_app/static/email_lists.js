/**********
 	The EmailLists singleton provides an interface to grab data about all the email lists a user is an administrator of.
**********/
function EmailLists(list_array)
{	
	this.lists = list_array;
	this.is_editing = false;
}

EmailLists.prototype = 
{
	end_editing : function()
	{
		if(!this.is_editing)
		{
			throw "Not editing a list!";
		}
		else
		{
			this.is_editing = false;
		}

		for(i = 0; i < this.lists.length; i++)
		{
			list = this.lists[i];
			if(list.is_editing)
			{
				this.validate_list_edit(list.get_list_id());
				list.is_editing = false;
			}
		}
	},

	start_editing : function(list_id)
	{
		if(this.is_editing)
		{
			return false;
		}

		this.is_editing = true;
		
		var list = this.get_list_by_id(list_id)
		if(!list)
		{
			throw "list does not exist!";
		}
		else
		{
			list.is_editing = true;
			return true;
		}
	},

	get_list_being_edited : function()
	{
		for(i = 0; i < this.lists.length; i++)
		{
			if(this.lists[i].is_editing)
			{
				return this.lists[i];
			}
		}

		return null;
	},

	get_list_by_name : function(name)
	{
		for(i = 0; i < this.lists.length; i++)
		{
			list = this.lists[i];
			if(list.list_name === name)
			{
				return list;
			}
		}
		
		return null;
	},

	//returns the amount of time between two formatted date strings "YYYY-MM-DD" in years
	get_date_delta : function(earlier_date_str, later_date_str)
	{
		//extract date components from arguments and put them into date objects
		var earlier_date_strs = earlier_date_str.split("-");
		var later_date_strs = later_date_str.split("-");

		var earlier_date = new Date(parseInt(earlier_date_strs[0]), 
									parseInt(earlier_date_strs[1]), 
									parseInt(earlier_date_strs[2]), 
									0, 0, 0);

		var later_date = new Date(parseInt(later_date_strs[0]),
								  parseInt(later_date_strs[1]), 
								  parseInt(later_date_strs[2]), 
								  0, 0, 0);

	    return (later_date.getTime() - earlier_date.getTime()) / (1000*60*60*24);
	},

	validate_list_edit : function(list_id)
	{
		var new_expire_date_str = $("form[name=edit_form] div[name=expire_date] input[name=expire_date]").val();

	    var current_expire_date = this.get_list_by_id(list_id).get_expire_date_str();

	    var delta_years = this.get_date_delta(current_expire_date, new_expire_date_str);

	    if(delta_years >= 2.0 || delta_years <= 0.0)
	    {
	        alert("Invalid expiration date!  Choose a date within two years of the current expiration date.");
	        return false;
	    }

	    return true;
	},

	get_list_by_id : function(id)
	{
		for(i = 0; i < this.lists.length; i++)
		{
			list = this.lists[i];
			if(list.list_id == id)
			{
				return list;
			}

			console.log(list.list_id);
		}

		throw("no list with id: ".concat(id));
	},
}

