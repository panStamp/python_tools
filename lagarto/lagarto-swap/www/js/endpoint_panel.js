/* Copyright (c) Daniel Berenguer (panStamp) 2012 */

/**
 * Create values
 */
function createValues()
{
  var jsonDoc = getJsonDoc();
  var swapnet = jsonDoc.lagarto;
  swapnet.status.forEach(addEndpoint);
}

/**
 * Add endpoint
 */
function addEndpoint(endpoint)
{
  var nettable = document.getElementById("nettable");
  var row, cell, label, command, val;
  row = nettable.insertRow(nettable.rows.length);

  // Endpoint ID
  cell = row.insertCell(0);
  label = document.createTextNode(endpoint.id);
  cell.appendChild(label);
  // Location
  cell = row.insertCell(1);
  label = document.createTextNode(endpoint.location);
  cell.appendChild(label);
  // Name
  cell = row.insertCell(2);
  label = document.createTextNode(endpoint.name);
  cell.appendChild(label);
  // Value
  cell = row.insertCell(3);
  val = document.createElement("input");
  val.type = "text";
  val.className = "w3-input-noedit";
  val.readOnly = "readOnly";
  val.id = endpoint.id;
  val.value = endpoint.value
  if ("unit" in endpoint)
  val.value += " " + endpoint.unit 
  cell.appendChild(val);
  // Time stamp
  val = document.createElement("input");
  val.type = "hidden";
  val.id = "ts_" + endpoint.id;
  val.value = endpoint.timestamp
  cell.appendChild(val);

  // Command
  cell = row.insertCell(4);

  // Edit button
	link = document.createElement("a");
  link.setAttribute("href", "/config_endpoint.html?id=" + endpoint.id);
  cell.appendChild(link);
  img = document.createElement("img");
  img.setAttribute("src","/lagarto/images/edit.png");
  img.title = "control";
  link.appendChild(img);

  if (endpoint.direction == "out")
  {
    // Control button
		link = document.createElement("a");
    link.setAttribute("href", "/control_endpoint.html?id=" + endpoint.id);
    cell.appendChild(link);
    img = document.createElement("img");
    img.setAttribute("src","/lagarto/images/control.png");
    img.title = "control";
    link.appendChild(img);
  }
}

/**
 * Update values
 */
function updateValues()
{
  var jsonDoc = getJsonDoc();
  var swapnet = jsonDoc.lagarto;
 
  swapnet.status.forEach(function(endpoint)
  {
    valField = document.getElementById(endpoint.id);
    if (valField != null)
    {
      valField.value = endpoint.value;
      if ("unit" in endpoint)
        valField.value += " " + endpoint.unit
    }
  });
}

