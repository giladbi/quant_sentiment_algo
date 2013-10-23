/*
get_rss_list.js

Takes in a list of rss feeds and returns an object of stories 
with metadata
*/

var request = require('request');
var fs = require('fs');
var xml = require('xml2js');
var processRssList = require('./process_rss_feed');

var CONFIG = require("../config.json");

var rssList = CONFIG.rss_feeds;
var outputFolder = CONFIG.output_folder;



//Process takes in a rss feed
rssList.forEach(function(feed){
	processRssList.processRssFeed(feed, function(xmlFeed){
		var xmlParsed = new xml.parseString(xmlFeed, handleXml);
	});
});

var handleXml = function(err, result) {

	var rssChannels = result.rss.channel;
	rssChannels.forEach(function(channel){
		// this item should usually have 1 item

		var sourceName = channel.title;
		var articles = channel.item;
		console.log("Source name: " + sourceName);
		for(var i=0; i<articles.length; i++){
			article = articles[i];
			var articleTitle = article.title[0];

			destPath = '.'+outputFolder+'/'+articleTitle+'.html';

			fetchUrl(article.link[0], destPath, function(err, data){

				fs.writeFile(data[1], data[0], function (err) {
				  if (err) throw err;
				  console.log('Succesfully wrote '+data[0].length+' to '+data[1]);
				});
			});

		}
	});
}

var fetchUrl = function(url, path, callback){
	urlFile = request(url, function(error, response, body){
		if(error) return callback(error);
		console.log("Downloading article from..."+url);
		body = [body, path];
		callback(null,body);
	});


};