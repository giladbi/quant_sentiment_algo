/*
get_rss_list.js

Takes in a list of rss feeds and returns an object of stories 
with metadata
*/
var request = require('request');
var xml = require('xml2js');

module.exports = processRssList = {
	processRssFeed: function(rssUrl, callback){
		/* 
		input: rss url
		output: json object with meta data
		*/
		console.log("Fetching RSS request for "+rssUrl);
		rssXml = request(rssUrl, function(error, response, body){
			if(error) return console.log(error);
			callback(body);
		});
	}
}
