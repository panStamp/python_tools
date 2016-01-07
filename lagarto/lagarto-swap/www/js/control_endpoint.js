/**
 * Update form fields
 */
function updateValues()
{
  var epid = getUrlVars()["id"];
  document.getElementById("endpid").value = epid;
}

/**
 * Submit control request
 */
function control(val)
{
  if (val != "")
    document.getElementById("value").value = val;
  else
    val = document.getElementById("value").value;

  var epid = document.getElementById("endpid").value
  var request = "values/?id=" + epid + "&value=" + val;
  loadJSONdata(request, received);
}

/**
 * Response received from server
 */
function received()
{
  window.location.href = "endpoint_panel.html";
}

