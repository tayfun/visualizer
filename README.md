Visualizer
=========

Simple project utilizing various Google App Engine features.

Takes 'text' parameter which is a simple text with links and fetches and parses the links. 

Both GET and POST methods work. Returned data is in json type for both methods. Shortened URLs work as AppEngine provides `final_url` for the urlfetch.fetch method.

Made use of BeautifulSoup for parsing HTML pages and pyjon for parsing and evaluating Javascript.


Retrieving Embed Codes
======================

Retrieving/parsing for embed codes is the most difficult part of this project. This is mainly because of the use of Javascript on the pages for generating these embed codes. For YouTube I simply had to use a template to return embed codes because I needed to execute javascript in the page to generate this code. For slideshare I could make use of PyJON library because embed codes were provided in a JSON object.

An optimal solution would be to use PhantomJS or another headless browser/javascript engine; although for this simple project it seemed an overkill. Ideally, V8 engine could parse and execute javascript in web pages and then we can retrieve the embed codes easily.


Testing
=======

I wrote a simple test which can be executed as

    python tests.py

Also, one can use the browser or curl to test the sample application which is hosted by Google App Engine. Simply browse to http://visualizer-demo.appspot.com/ . For example: [test using shortened URLs](http://visualizer-demo.appspot.com/visualize.php?text=Check%20out%20this%20video%20of%20Eric%20Ries%20http://bit.ly/aVlV11%20from%20Stanford%20University.%20It's%20a%20good%20start%20to%20understand%20Lean%20Startup.%20Here%20is%20a%20presentation%20http://slidesha.re/M2z64S%20NYTIme%20recently%20covered%20him%20too%20http://nyti.ms/aICucz)

For testing through the browser you can utilize JSONView plugin for chrome which pretty prints the JSON output; this plugin can be utilized because the header is correctly set. One can also use curl:

    curl -X POST -d "text=Check%20out%20this%20video%20of%20Eric%20Ries%20http://bit.ly/aVlV11%20from%20Stanford%20University.%20It's%20a%20good%20start%20to%20understand%20Lean%20Startup.%20Here%20is%20a%20presentation http://slidesha.re/M2z64S NYTIme recently covered him too http://nyti.ms/aICucz" http://visualizer-demo.appspot.com/visualize.php -v | python -m json.tool

Note that I haven't changed the php extension even though it is written in Python :)

Also note that incomplete links such as `youtube.com/watch?v=ajSzCtwTj_I` also works:

    curl -X POST -d "text=youtube.com/watch?v=ajSzCtwTj_I" http://visualizer-demo.appspot.com/visualize.php -v | python -m json.tool

