import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class SetupBrowser:


	def __init__(self):
		self.driver = None

	def setupChromeBorwser(self):
		self.driver = webdriver.Chrome()
		self.driver.maximize_window()
		#self.driver.set_window_rect(x, y, width, height)
		self.driver.implicitly_wait(5)
		#time.sleep(5)

	# open the link in the browser
	def openLink(self, url):
		self.driver.get(url)
		time.sleep(5)

class Flipkart(SetupBrowser):

	# skip the pop-up for login
	def skipLogin(self):
		self.driver.find_element_by_css_selector('button._2AkmmA._29YdH8').click()
		time.sleep(5)

	# login to the website
	def login(self, mobileNo, password):
		self.driver.find_element_by_xpath('//*[@class="_2zrpKA _1dBPDZ"]')\
			.send_keys(mobileNo)
		self.driver.find_element_by_xpath('//*[@class="_2zrpKA _3v41xv _1dBPDZ"]')\
			.send_keys(password)
		self.driver.find_element_by_xpath('//*[@class="_2AkmmA _1LctnI _7UHT_c"]')\
			.click()
		time.sleep(5)

	# search the product
	def searchProduct(self, value):
		elem = self.driver.find_element_by_class_name('LM6RPg')
		elem.send_keys(value)
		elem.send_keys(Keys.ENTER)
		time.sleep(5)

	# set the color filter in the searched list
	def selectColor(self, color):
		self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]'
										  '/div[1]/div/div/div/section[6]/div[2]/div[2]'
										  '/span').click()
		time.sleep(2)
		self.driver.find_element_by_xpath('//*[@title="'+ color +'"]/div/div/label/div[1]').click()
		time.sleep(5)

	def addToCart(self):
		shoeSizes = self.driver.find_elements_by_xpath('//*[@class="_1TJldG _2I_hq9 _2UBURg"]') # list of the shoes size
		for i in shoeSizes:
			if i.value_of_css_property('color') == 'rgba(33, 33, 33, 1)':
				i.click()
				time.sleep(3)
				break

		self.driver.find_element_by_xpath('//*[@class="_2AkmmA _2Npkh4 _2MWPVK"]').click()
		time.sleep(5)

	# select the n product form the start (n = quantity)
	def selectProduct(self, quantity):
		productList = self.driver.find_elements_by_xpath('//*[@class="_3ZJShS _31bMyl"]')
		for prod in productList[:quantity]:
			prod.click()
			time.sleep(2)

			self.driver.switch_to.window(self.driver.window_handles[1])
			self.addToCart()
			self.driver.close()

			self.driver.switch_to.window(self.driver.window_handles[0])
			time.sleep(2)
			
	# set the address form for order
	def setAddress(self, name, mobileNo, pinCode, locality, address):
		self.driver.find_element_by_name('name').send_keys(name)
		self.driver.find_element_by_name('phone').send_keys(mobileNo)
		self.driver.find_element_by_name('pincode').send_keys(pinCode)
		self.driver.find_element_by_name('addressLine2').send_keys(locality)
		self.driver.find_element_by_name('addressLine1').send_keys(address)
		self.driver.find_element_by_xpath('//*[@class="_2AkmmA EqjTfe _7UHT_c"]').click()


	def placeOrder(self):
		self.driver.find_element_by_xpath('//*[@class="_3ko_Ud"]').click()
		time.sleep(5)
		self.driver.find_element_by_xpath('//*[@class="_2AkmmA iwYpF9 _7UHT_c"]').click()
		time.sleep(5)

		try:
			# More then two address are present
			self.driver.find_element_by_xpath('//*[@class="_2Y8lQ1"]').click()
			time.sleep(1)
			self.setAddress('Gaurav' , '8109581512', '482004', 'Adhartal', 'phot no 60')


		except NoSuchElementException:

			try:
				# Only one address is present in the user-id
				self.driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div/div/div[2]/div/div/button').click()
				self.driver.find_element_by_xpath('//*[@class="_2Y8lQ1"]').click()

				time.sleep(2)
				self.setAddress('Gaurav' , '8109581512', '482004', 'Adhartal', 'phot no 60')

			except NoSuchElementException:
				# No address is already present
				self.driver.find_element_by_xpath('//*[@class="_3llGqN"]')
				time.sleep(2)
				self.setAddress('Gaurav' , '8109581512', '482004', 'Adhartal', 'phot no 60')


width = 680
height = 368
def main():
	# lock.acquire()
	# global  threadCount
	# x = 0
	# y = 0
	# if threadCount == 2:
	# 	x = width
	# elif threadCount == 3:
	# 	y = height
	# elif threadCount == 4:
	# 	x = width
	# 	y = height
	#
	# threadCount = threadCount + 1
	# lock.release()

	username = input('Flipkart Login [Mobile No] : ')
	password = input('Password : ')

	Driver = Flipkart()
	Driver.setupChromeBorwser()
	Driver.openLink('https://www.flipkart.com/')
	#Driver.skipLogin()
	Driver.login(username, password)
	Driver.searchProduct('white shoes')
	Driver.selectColor('White')
	Driver.selectProduct(1)
	Driver.placeOrder()
	Driver.driver.close()

main()

# lock = threading.Lock()

# threadCount = 1
# thread1 = threading.Thread(target=main, args=(lock,))
# thread1.start()
#
# thread2 = threading.Thread(target=main, args=(lock,))
# thread2.start()
#
# thread3 = threading.Thread(target=main, args=(lock,))
# thread3.start()
#
# threading.Thread(target=main, args=(lock,)).start()


