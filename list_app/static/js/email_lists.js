/**********
 	The EmailLists singleton provides an interface to grab data about all the email lists a user is an administrator of.
**********/
function EmailLists(list_array)
{	
	this.lists = list_array;
	this.is_editing = false;
	this.cached_list = null; //use this this to store a copy of a list being edited so that it can be reset if it doesn't validate correctly
}

EmailLists.prototype = 
{
	cancel_editing : function()
	{
		if(!this.is_editing)
		{
			throw "Not editing a list!";
		}
		
		this.is_editing = false;

		for(i = 0; i < this.lists.length; i++)
		{
			list = this.lists[i];
			if(list.is_editing)
			{
				this.cached_list = null;
				this.is_editing = false;
				list.is_editing = false;
			}
		}
	},

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
				if(!this.validate_list_edit(list.get_list_id()))
				{
					this.is_editing = false;
					list.is_editing = false;
					return;
				}
				else
				{
					var list_id = list.get_list_id();
					var form = $("form[id=edit_form_".concat(list_id).concat("]"));
					form.submit();

					this.cached_list = null;
					this.is_editing = false;
					list.is_editing = false;
				}
			}
		}
	},

	start_editing : function(id)
	{
		if(this.is_editing)
		{
			return false;
		}

		this.is_editing = true;
		
		var list = this.get_list_by_id(id)
		if(!list)
		{
			throw "list does not exist!";
			this.is_editing = false;
		}
		else
		{
			list.is_editing = true;
			this.cached_list = list.clone();

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

	//returns the amount of time between two formatted date strings "YYYY-MM-DD" in days
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
		var new_expire_date_str = $("form[id=edit_form_".concat(list_id).concat("] input[name=expire_date]")).val();

	    var current_date = new Date();
	    current_date_str = String(current_date.getFullYear()).concat("-").concat(String(current_date.getMonth())).concat("-").concat(String(current_date.getDate()));

	    var delta_days = this.get_date_delta(current_date_str, new_expire_date_str);

	    if(delta_days > 731.0 || delta_days <= 0.0)
	    {
	        alert("Invalid expiration date!  Choose a date within two years of the current date.");
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
		}

		throw("no list with id: ".concat(id));
	},
}

