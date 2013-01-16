Synonymiser
===========

##Description

Takes text input from the user and returns it with each word replaced by a synonym.

##Variations

This repositiory contains two different versions - a local only version that pulls all
its data from a local thesaurus, or a (better/more accurate) online version that pulls
data from a web api.

###Which should I use?

The online version uses more accurate data, uses less RAM (under normal use), and doesn't 
require downloading a large thesaurus file for use. It does however, require an internet
connection and can be a little slower as it needs to fetch its results online - this 
process is alleviated by caching, becoming quicker with extended use.

My suggestion is to only use the local version if an internet connection is unavailable.
Local version requires the thesaurus file available [here.](http://www.gutenberg.org/dirs/etext02/mthes10.zip)

##Usage

When run the user will be prompted with `>>`. Once some text is entered and the user has 
pressed `enter`, a 'synonymized' version of the text will be returned.

###Example

> `>>` A person who never made a mistake never tried anything new.
> `A organism who on no condition brought about a gaucherie to the contrary tried anything extra.`

##To Do

###Online Version
* Fix cli use
* Possibly improve efficiency of api use
* Introduce natural language processing for syntactic parsing

###Local Version
* Reduce memory requirements for (thesaurus currently stored in dictionary)
* Find a better thesaurus