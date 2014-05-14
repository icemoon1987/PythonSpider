/** Download a image from a web page

 The url is the first parameter
 The file name to be stored is the thired parameter
 */

var system = require('system');

var url = system.args[1];
var file = system.args[2];

var page = require('webpage').create();

page.settings.resourceTimeout = 60000;

page.onResourceTimeout = function(e) {
  console.log(e.errorCode);   // it'll probably be 408 
  console.log(e.errorString); // it'll probably be 'Network timeout on resource'
  console.log(e.url);         // the url whose request timed out
};

page.open(url, function(status) {

	if(status == "success")
	{
		if( page.injectJs('jquery-1.10.2.min.js') == true )
        {
        }
        else
        {
        	console.log("Inject jQuery Failed!");
			phantom.exit();
        }

        var image = page.evaluate(function() {

        	var image = new Object();

        	$("img#img").each(function() {
        		image.top = $(this).offset().top,
				image.left = $(this).offset().left,
				image.width = $(this).width(),
				image.height = $(this).height()
        	})

        	return image;
        });

        page.clipRect = image;

        page.render(file);

        phantom.exit();

	}
	else
	{
		console.log("Open url: " + url + " error!");
		phantom.exit();
	}

});


