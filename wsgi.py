"""
/*-------------------------------------------------------------------*/
/*                                                                   */
/* Copyright IBM Corp. 2013 All Rights Reserved                      */
/*                                                                   */
/*-------------------------------------------------------------------*/
/*                                                                   */
/*        NOTICE TO USERS OF THE SOURCE CODE EXAMPLES                */
/*                                                                   */
/* The source code examples provided by IBM are only intended to     */
/* assist in the development of a working software program.          */
/*                                                                   */
/* International Business Machines Corporation provides the source   */
/* code examples, both individually and as one or more groups,       */
/* "as is" without warranty of any kind, either expressed or         */
/* implied, including, but not limited to the warranty of            */
/* non-infringement and the implied warranties of merchantability    */
/* and fitness for a particular purpose. The entire risk             */
/* as to the quality and performance of the source code              */
/* examples, both individually and as one or more groups, is with    */
/* you. Should any part of the source code examples prove defective, */
/* you (and not IBM or an authorized dealer) assume the entire cost  */
/* of all necessary servicing, repair or correction.                 */
/*                                                                   */
/* IBM does not warrant that the contents of the source code         */
/* examples, whether individually or as one or more groups, will     */
/* meet your requirements or that the source code examples are       */
/* error-free.                                                       */
/*                                                                   */
/* IBM may make improvements and/or changes in the source code       */
/* examples at any time.                                             */
/*                                                                   */
/* Changes may be made periodically to the information in the        */
/* source code examples; these changes may be reported, for the      */
/* sample code included herein, in new editions of the examples.     */
/*                                                                   */
/* References in the source code examples to IBM products, programs, */
/* or services do not imply that IBM intends to make these           */
/* available in all countries in which IBM operates. Any reference   */
/* to the IBM licensed program in the source code examples is not    */
/* intended to state or imply that IBM's licensed program must be    */
/* used. Any functionally equivalent program may be used.            */
/*-------------------------------------------------------------------*/
"""

import bottle
from bottle import *
import os,sys,logging, traceback, json, string, urllib, urllib2
import pymongo
from pymongo import *
from pymongo import Connection

from BeautifulSoup import BeautifulSoup
import httplib2

# Configs from BlueMix 
vcap_config = os.environ.get('VCAP_SERVICES')
decoded_config = json.loads(vcap_config)

for key, value in decoded_config.iteritems():
	if key.startswith('mongo'):
		mongo_creds = decoded_config[key][0]['credentials']

# ---- configuring mongo ---- 
mongo_url = str(mongo_creds['uri'])
client = pymongo.Connection(mongo_url)
mongo_db = mongo_url.split('@')[1].split('/')[1]

mongoDB = client[mongo_db]
itemCollection = mongoDB["ItemCollection"]
# ---- end of mongo config ---- 


#Provide all the static css and js files under the static dir to browser
@route('/static/:filename#.*#')
def server_static(filename):
	""" This is for JS files """
	return static_file(filename, root='static')

# Displays the home page
@bottle.get("/")
def testFunc():
	return bottle.template('home')
	
# Get the prices for all of the items stored in the database
@bottle.get('/getCurrentPrices')		
def getCurrentPrices():
	items = itemCollection.find()

	for item in items:
		getCurrentPrice(item)
		
	return bottle.template('currentPrice')

# Get the current price of a particular item
def getCurrentPrice(item):
	
	try: 			
		http = httplib2.Http()
		status, page = http.request(item["url"])
		soup = BeautifulSoup(page)
		price = soup.find(id=item["idToCheck"]).string	
		
		if price is not None:
			
			itemCollection.update({'url': item["url"]},{"$set" : {'price':price}})
			
			return bottle.template('currentPrice', price=price)
		
		else:
			return bottle.template('currentPriceError')
	except:
		return bottle.template('currentPriceError')

# Saves the item info in the database
@bottle.post('/recordItemInfo')
def recordItemInfo():

	name = request.forms.get('name')
	url = request.forms.get('url')
	idToCheck = request.forms.get('idToCheck')
	
	existTest = itemCollection.find({'url': url}).count()
	if existTest == 0:
		data = {'url': url, 'name': name,'idToCheck': idToCheck}
		insert_id = itemCollection.insert(data)
		print "Data inserted"
	else:
		itemCollection.update({'url': url},{"$set" : {'name':name}})
		itemCollection.update({'url': url},{"$set" : {'idToCheck':idToCheck}})
		print "Data updated"
	cursor = list(itemCollection.find())
	totinf = int(itemCollection.count())

	return bottle.template ('dbdump',totinf=totinf,cursor=cursor)


#  Displays all the records in the database
@bottle.get('/displayall')
def displayData():
	cursor = list(itemCollection.find())
	totinf = int(itemCollection.count())
	
	return bottle.template ('dbdump',totinf=totinf,cursor=cursor)

# Removes all the records from the database
@bottle.post('/clearall')
def clearAll():
	itemCollection.remove()
	cursor = list(itemCollection.find())
	totinf = int(itemCollection.count())
	print "this is the value: %d" % totinf
	return bottle.template ('dbdump',totinf=totinf,cursor=cursor)


# Removes only the selected stuff from the database
@bottle.post('/delselected')
def removeSelected():
	s = str(request.forms.get('url'))
	itemCollection.remove({'url' : s})
	cursor = list(itemCollection.find())
	totinf = int(itemCollection.count())
	print "this is the value: %d" % totinf
	return bottle.template ('dbdump',totinf=totinf,cursor=cursor)

debug(True)

# Error Methods
@bottle.error(404)
def error404(error):
    return 'Nothing here--sorry!'


application = bottle.default_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    bottle.run(host='0.0.0.0', port=port)
