document.write("<nav class='w3-sidenav w3-white w3-card-2' style='display:none'>");
document.write("  <a href='javascript:void(0)' onclick='w3_close()' class='w3-closenav w3-large'>Close &times;</a>");
document.write("  <a href='/general_settings.html'>General settings</a>");
document.write("  <a href='/lagarto/lagarto_settings.html'>MQTT/HTTP settings</a>");
document.write("  <a href='/modem_serial.html'>Serial gateway</a>");
document.write("  <a href='/modem_network.html'>SWAP settings</a>");
document.write("  <a href='/device_panel.html'>Device panel</a>");
document.write("  <a href='/endpoint_panel.html'>Endpoint panel</a>");
document.write("  <a href='/lagarto/account_panel.html'>Security</a>");
document.write("</nav>");

function setTitle(title)
{
  document.write("<header class='w3-container w3-theme'>");
  document.write("  <table><tr><td width='1%'>");
  document.write("    <img class='w3-opennav' onclick='w3_open()' src='/lagarto/images/reorder.png'></img>");
  document.write("    </td><td>");
  document.write("    <h3>&nbsp;" + title + "</h3></td></tr>");
  document.write("  </table>");
  document.write("</header>");
}

function w3_open() {
    document.getElementsByClassName("w3-sidenav")[0].style.display = "block";
}
function w3_close() {
    document.getElementsByClassName("w3-sidenav")[0].style.display = "none";
}

