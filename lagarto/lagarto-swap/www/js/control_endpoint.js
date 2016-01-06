/**
 * Update form fields
 */
function updateValues()
{
  var endpid = getUrlVars()["id"];
  document.getElementById("endpid").value = endpid;
}

/**
 * Submit control request
 */
function control(val)
{
  document.getElementById("value").value = val
  document.getElementById("dataform").submit()
}

