from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class BrowserSetup:
	def __init__(self):
		driver = None

	# setup the chrome browser
	def setupChromeBrowser(self):
		self.driver = webdriver.Chrome()
		self.driver.maximize_window()
		time.sleep(5)	
		

	def openLink(self, url):
		self.driver.get(url)
		time.sleep(5)
	

class Goibibo(BrowserSetup):

	# select the source place
	def source(self,src):
		elem = self.driver.find_element_by_id("gosuggest_inputSrc")
		elem.send_keys(src)
		time.sleep(2)
		elem.send_keys(Keys.DOWN)
		elem.send_keys(Keys.ENTER)

	# select the destination place
	def destination(self, dest):
		elem = self.driver.find_element_by_id("gosuggest_inputDest")
		elem.send_keys(dest)
		time.sleep(2)
		elem.send_keys(Keys.DOWN)
		elem.send_keys(Keys.ENTER)

	# select the departure date 
	def setDepDate(self, date):
		
		# select the no of month left to depart
		month = {'January':1, 'February':2, 'March':3, 'April':4, 'May': 5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
		currentMonth = self.driver.find_element_by_xpath('//*[@class="DayPicker-Caption"]').text.split()[0]
		monthsToDep = int(date[4:6]) - month.get(currentMonth)


		date = 'fare_' + date
		
		elem = self.driver.find_element_by_css_selector('span.DayPicker-NavButton.DayPicker-NavButton--next')
		for i in range(monthsToDep):
			elem.click()
		
		self.driver.find_element_by_id(date).click()
		

	# select the return date
	def setReturnDate(self, date):
		# calculate the duration of the trip in months
		month = {'January':1, 'February':2, 'March':3, 'April':4, 'May': 5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
		elem = self.driver.find_element_by_id('returnCalendar').click()
		currentMonth = self.driver.find_element_by_xpath('//*[@class="DayPicker-Caption"]').text.split()[0]
		tripDuration = int(date[4:6]) - month.get(currentMonth)

		date = 'fare_' + date

		# select the correct month for the return date
		elem = self.driver.find_element_by_css_selector('span.DayPicker-NavButton.DayPicker-NavButton--next')
		for i in range(tripDuration):
			elem.click()
		
		elem = self.driver.find_element_by_id(date).click()


	def searchFlight(self):
		self.driver.find_element_by_id('gi_search_btn').click()
		time.sleep(5)

	def BookFlight(self):
		self.driver.find_element_by_css_selector('input.button.fr.fltbook.fb.widthF105.quicks.fb').click()
		time.sleep(5)

	# tick the check box for assurance
	def selectTravelAssurance(self, val):
		if val == True:
			self.driver.find_element_by_id('secure-trip').click()
		else:
			self.driver.find_element_by_id('risk-trip').click()

	# set the passenger details
	def setPassengerDetail(self, firstName, lastName, email, mobileNo):
		# select the title 'Mr'
		self.driver.find_element_by_id('Adulttitle1').click()
		self.driver.find_element_by_xpath('//*[@id="Adulttitle1"]/option[2]').click()

		# select the first name in the field
		self.driver.find_element_by_id('AdultfirstName1').send_keys(firstName)
		
		# select the last name in the field
		self.driver.find_element_by_id('AdultlastName1').send_keys(lastName)
		
		# select the email address
		self.driver.find_element_by_id('email').send_keys(email)
		
		# select the mobile number
		self.driver.find_element_by_id('mobile').send_keys(mobileNo)
		
	def proceed(self):
		self.driver.find_element_by_css_selector('button.orange.col-md-3.fr.large.dF.justifyCenter.min37').click()
		time.sleep(5)

	def proceedToPayment(self):
		self.driver.find_element_by_css_selector('button.width100.ico14.padLR20.white.button.hpyOrangeBg.large.txtCenter.marginT15.brdrTLR0.padTB5.bkPgPrcd').click()



driver = Goibibo()
driver.setupChromeBrowser()
driver.openLink('https://www.goibibo.com/')
driver.source("Pune")
driver.destination("Nagpur")
driver.setDepDate('20200515')
driver.setReturnDate('20200715')
driver.searchFlight()
driver.BookFlight()
driver.selectTravelAssurance(True)
driver.setPassengerDetail('Gaurav', 'Verma', 'gourav10verma@gmail.com', '8109581512')
driver.proceed()
driver.proceedToPayment()
