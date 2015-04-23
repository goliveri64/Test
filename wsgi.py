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

from BeautifulSoup import BeautifulSoup
import httplib2

import cloudant
import pprint
import urllib

# Configs from BlueMix 
vcap_config = os.environ.get('VCAP_SERVICES')
decoded_config = json.loads(vcap_config)

dbname = "fabulous-price-finder"
account = None

for key, value in decoded_config.iteritems():
	if key.startswith('cloudant'):
		cloudant_creds = decoded_config[key][0]['credentials']
		cloudant_host = cloudant_creds['host']
		cloudant_port = int(cloudant_creds['port'])
		cloudant_username = cloudant_creds['username']
		cloudant_password = cloudant_creds['password']
		cloudant_url = str(cloudant_creds['url'])
		
		account = cloudant.Account(cloudant_username)
		login = account.login(cloudant_username, cloudant_password)
		assert login.status_code == 200
		
		db = account.database(dbname)
		
		response = db.put()
		print response.json


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
		
	z = []
	view = db.all_docs()
	for doc in view.iter(params={'include_docs': True}):
		getCurrentPrice(doc['doc'])
		pass
		
	return bottle.template('currentPrice')

# Get the current price of a particular item
def getCurrentPrice(item):
	
	try: 			
		http = httplib2.Http()
		status, page = http.request(urllib.unquote_plus(item["url"]))
		soup = BeautifulSoup(page)
		price = soup.find(id=item["idToCheck"]).string	
		
		if price is not None:
			
			d = db.document(item["url"])
			resp = d.merge({ 'url': item["url"], 'price': price})
			

			return bottle.template('currentPrice', price=price)
		
		else:
			return bottle.template('currentPriceError')
	except:
		return bottle.template('currentPriceError')

# Saves the item info in the database
@bottle.post('/recordItemInfo')
def recordItemInfo():

	name = str(request.forms.get('name'))
	url = urllib.quote_plus(request.forms.get('url'))

	idToCheck = str(request.forms.get('idToCheck'))
	
	# get document
	d = db.document(url)
	# merge updated information
	resp = d.merge({ 'url': url, 'name': name, 'idToCheck': idToCheck})

	bottle.redirect('/displayall')


#  Displays all the records in the database
@bottle.get('/displayall')
def displayData():
	z = []
	view = db.all_docs()
	for doc in view.iter(params={'include_docs': True}):
		z.append(doc['doc'])
		pass
	cursor = list(z)
	totinf = int(len(cursor))

	return bottle.template ('dbdump',totinf=totinf,cursor=cursor)

# Removes all the records from the database
@bottle.post('/clearall')
def clearAll():
	# destroy DB
	del account[dbname]
	# recreate DB
	# bug: the db is not getting recreated 
	db = account.database(dbname)
	return bottle.template ('dbdump',totinf=0,cursor=[])


# Removes only the selected stuff from the database
@bottle.post('/delselected')
def removeSelected():
	s = urllib.quote_plus(request.forms.get('url'))
	# document we want to delete
	del_doc = db.document(s)
	
	# iterate over all documents to find revision # for one we want to delete
	view = db.all_docs()
	for doc in view.iter(params={'include_docs': True}):
		if (doc['doc']['url'] == s):
			rev = doc['doc']['_rev']
			del_doc.delete(rev).raise_for_status()
			
	bottle.redirect('/displayall')
	


debug(True)

# Error Methods
@bottle.error(404)
def error404(error):
    return 'Nothing here--sorry!'


application = bottle.default_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    bottle.run(host='0.0.0.0', port=port)
