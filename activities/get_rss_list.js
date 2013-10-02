/*
get_rss_list.js

Takes in a list of rss feeds and returns an object of stories 
with metadata
*/

var request = require('request');
var xml = require('xml2js');
var processRssList = require('./process_rss_feed');

var CONFIG = require("../config.json");

var rssList = CONFIG.rss_feeds;

rssList.forEach(function(feed){
	processRssList.processRssFeed(feed, function(xmlFeed){
		var xmlParsed = new xml.parseString(xmlFeed, handleXml);
	});
});

var handleXml = function(err, result) {
	console.log(result.rss.channel[0].item);
}