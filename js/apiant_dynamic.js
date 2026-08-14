// NOTE: this file is now maintained in the apiant-website repo (js/apiant_dynamic.js)
// and deployed by the website CI. The HubSpot chat widget loader that used to live
// here was removed on purpose; the site no longer offers live chat.

function replace(sText, sFind, sReplace)
{
    if (sText != null && typeof(sText) == "string")
    {
        var arr = sText.split(sFind);
        return arr.join(sReplace);
    }
    else return sText;
}

function getCookie(name)
{
	var cookie = document.cookie;
	var prefix = name + '*';
	var i = cookie.indexOf(prefix);
	if (i == -1) return null;
	var j = cookie.indexOf("&", i + prefix.length);
	if (j == -1) j = cookie.length;
	return unescape(cookie.substring(i + prefix.length, j));
}

function updatePageState()
{
	if (getCookie("person_uuid") != null && getCookie("person_uuid").length > 0)
	{
		if (typeof global != 'undefined' && global["FS"])
        {
            FS.identify(getCookie("person_uuid"), {displayName: replace(getCookie("person_fullname"), "_", " "), email: getCookie("person_email")});
        }
        
	
		var arr = document.getElementsByClassName("login-link");
		for (var i=0; i<arr.length; i++)
		{
			arr[i].style.display = "none";
		}
		
		var isHomepage = window.location.href == "https://apiant.com" || window.location.href.indexOf("index") != -1;
		
		var strPlanId = getCookie("subscription_plan_id");	
		if (strPlanId != null && strPlanId.length > 0)
		{
			var isYearlyPlan = strPlanId.lastIndexOf("10") == strPlanId.length-2;
			
			var subscription_plan_id = parseInt(strPlanId);
			if (subscription_plan_id < 0)
			{
				arr = document.getElementsByClassName("new-visitor");
				for (var i=0; i<arr.length; i++)
				{
					if (isHomepage)
					{
						var className = arr[i].childNodes[0].className; 
						var pos = className ? className.indexOf("planid-") : -1;
						if (pos != -1)
						{
							var button_plan_id = parseInt(className.substring(pos+7, className.indexOf(" ", pos)));
							if (button_plan_id == 10000 && subscription_plan_id != -200)
							{
								arr[i].style.display = "flex";
							}
							else if (button_plan_id == 20000 && subscription_plan_id != -201)
							{
								arr[i].style.display = "flex";
							}
							else if (button_plan_id == 30000 && subscription_plan_id != -202)
							{
								arr[i].style.display = "flex";
							}
							else
							{
								arr[i].style.display = "none";
							}
						}
						else
						{
							arr[i].style.display = "none";
						}
					}
					else
					{
						arr[i].style.display = "none";
					}
				}
				
				arr = document.getElementsByClassName("trial-visitor");		
				for (var i=0; i<arr.length; i++)
				{
					arr[i].style.display = arr[i].className.indexOf("apiantbutton") == -1 ? "block" : "flex";
				}
			}
			else
			{
				arr = document.getElementsByClassName("new-visitor");
				for (var i=0; i<arr.length; i++)
				{
					arr[i].style.display = "none";
				}
			
				arr = document.getElementsByClassName("subscribed-visitor");			
				for (var i=0; i<arr.length; i++)
				{
					arr[i].style.display = arr[i].className.indexOf("apiantbutton") == -1 ? "block" : "flex";
				}
				
				arr = document.body.getElementsByTagName("*");
				for (var i=0; i<arr.length; i++)
				{
                    if (arr[i].className.indexOf != undefined)
                    {
        					var pos = arr[i].className.indexOf("planid-");
        					if (pos != -1)
        					{
        						var button_plan_id = parseInt(arr[i].className.substring(pos+7, arr[i].className.indexOf(" ", pos)));
        						
        						if (button_plan_id == subscription_plan_id)
        						{
        							if (arr[i].className.indexOf("button-type-current") != -1)
        							{
        								arr[i].style.display = arr[i].className.indexOf("apiantbutton") == -1 ? "block" : "flex";
        								arr[i].style.cursor = "not-allowed";
        							}
        							else
        							{
        								arr[i].style.display = "none";
        							}
        						}
        						else if (subscription_plan_id-button_plan_id == -10 || subscription_plan_id-button_plan_id == 10)
        						{
        							if (arr[i].className.indexOf("button-type-switch-billing") != -1)
        							{
        								arr[i].style.display = arr[i].className.indexOf("apiantbutton") == -1 ? "block" : "flex";
        							}
        							else
        							{
        								arr[i].style.display = "none";
        							}
        						}
        						else if (button_plan_id < subscription_plan_id)
        						{
        							if (arr[i].className.indexOf("button-type-downgrade") != -1)
        							{
        								arr[i].style.display = arr[i].className.indexOf("apiantbutton") == -1 ? "block" : "flex";
        							}
        							else
        							{
        								arr[i].style.display = "none";
        							}
        						}
        						else if (button_plan_id > subscription_plan_id)
        						{
        							if (arr[i].className.indexOf("button-type-upgrade") != -1)
        							{
        								arr[i].style.display = arr[i].className.indexOf("apiantbutton") == -1 ? "block" : "flex";
        							}
        							else
        							{
        								arr[i].style.display = "none";
        							}
        						}
        					}
                    }
					
					if (subscription_plan_id >= 14000 && subscription_plan_id < 20000)
					{
						if (arr[i].className == "next-plans w-row" || arr[i].className == "next-plans-table" || arr[i].className == "previous-plans-link")
						{
							arr[i].style.display = arr[i].className.indexOf("apiantbutton") == -1 ? "block" : "flex";
						}
						else if (arr[i].className == "base-plans w-row" || arr[i].className == "base-plans-table" || arr[i].className == "next-plans-link")
						{
							arr[i].style.display = "none";
						}
					}
					
					if (isYearlyPlan)
					{
						if (arr[i].className == "yearly-plans" || arr[i].className == "monthly-plan-link")
						{
							arr[i].style.display = arr[i].className.indexOf("apiantbutton") == -1 ? "block" : "flex";
						}
						else if (arr[i].className == "monthly-plans" || arr[i].className == "yearly-plan-link")
						{
							arr[i].style.display = "none";
						}
					}
				}
			}
		}
		else
		{
//			alert("Ouch, something is wrong.  We can see you have an account, but can't determine your subscription status.  Try signing out of the system and signing back in again.");
		}
	}
}

updatePageState();