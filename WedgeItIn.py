# Chuck's Jython Swing Examples used to learn Jython
# Copyright(c) 2007 Chuck Hutchinson - Developed under the funding of a Night's and Weekend's Project - Otherwise known as a NAW project!
import java.lang.Exception as Exception
import java.lang.Thread as Thread
import java.lang.Runnable as Runnable
import java.lang.Math as Math
import java.lang.System as System
import java.lang.Integer as Integer
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.awt.Color as Color
import java.awt.Font as Font
import java.awt.Dimension as Dimension
import java.awt.GridLayout as GridLayout
import java.awt.GridBagConstraints  as GridBagConstraints
import java.awt.GridBagLayout  as GridBagLayout
import java.awt.BorderLayout as BorderLayout
import java.awt.Panel as Panel
import java.awt.Dialog as Dialog
import java.awt.Window as Window
import java.awt.print.Printable as Printable
import java.awt.print.PageFormat as PageFormat
import java.awt.print.PrinterJob as PrinterJob
import java.awt.Component as Component
import javax.swing as swing
import javax.swing.UIManager as UIManager
import javax.swing.JComponent as JComponent
import javax.swing.JFileChooser as JFileChooser
import javax.swing.JPanel as JPanel
import javax.swing.JLabel as JLabel
import javax.swing.JSpinner as JSpinner
import javax.swing.BoxLayout as BoxLayout
import javax.swing.BorderFactory as BorderFactory
import javax.swing.JDialog as JDialog
import javax.swing.JFrame as JFrame
import javax.swing.JScrollPane as JScrollPane
import javax.swing.JTextPane as JTextPane
import javax.swing.JTable as JTable
import javax.swing.JButton as JButton
import javax.swing.JTabbedPane as JTabbedPane
import javax.swing.JEditorPane as JEditorPane
import javax.swing.JTextField as JTextField
import javax.swing.SpringLayout as SpringLayout
import javax.swing.ScrollPaneLayout as ScrollPaneLayout
import javax.swing.ImageIcon as ImageIcon
import javax.swing.SwingUtilities as SwingUtilities
import javax.swing.event.HyperlinkEvent as HyperlinkEvent
import javax.swing.event.HyperlinkListener as HyperlinkListener
import javax.swing.RepaintManager as RepaintManager
import javax.swing.filechooser.FileFilter as FileFilter
import java.net.URL as URL
import java.net.UnknownHostException as UnknownHostException
import java.net.Socket as Socket
import java.net.InetAddress as InetAddress
import java.net.InetSocketAddress as InetSocketAddress
import java.net.MulticastSocket as MulticastSocket
import java.net.DatagramPacket as DatagramPacket
import java.util.Vector as Vector
import java.util.Date as Date
import java.io.BufferedReader as BufferedReader
import java.io.InputStreamReader as InputStreamReader
import java.io.File as File
import java.io.FileOutputStream as FileOutputStream
import java.io.PrintStream as PrintStream
import java.nio.charset.Charset as Charset
import java.text.DateFormat as DateFormat
import sys

def readSocket(host, port):
	try:
		print 'connecting to host/port' + host + ' port ' 
		print port
		print '\n'
		s = Socket(host, port)
		o = BufferedReader(InputStreamReader(s.getInputStream(), Charset.forName("UTF-8")))
		
		results = ''
		while 1:
			line = o.readLine()
			print 'line: ' + line + '\n'
			results = results + line + '\n'
			if not line:
				break
		
		return	results
	except Exception, e:
		return e.message

def readFile(filename):
	try:
            contents = ''
            f = open(filename, 'r')
            for line in f:
            	contents = contents + line
            	
            return contents
				
	except Exception: 
		return 'Unable to open file: ' + filename

class SnapPanel(JPanel):

	def __init__(self, innerPanel):
		JPanel.__init__(self)
		self.layout = GridLayout(0,1)
		self.control = JScrollPane(innerPanel)
		self.add(self.control)	

class TopPanel(JPanel):
	def __init__(self, innerPanel, title):
		self.layout = BorderLayout()
		self.add(SnapPanel(innerPanel), BorderLayout.NORTH)	
		self.border = BorderFactory.createCompoundBorder(
			BorderFactory.createTitledBorder(title), 
			BorderFactory.createEmptyBorder(10,10,10,10))

class CFDialog(JDialog):

	def __init__(self, dialogTitle, innerPanel):
		JDialog.__init__(self)
		# Dialog.setTitle(self, dialogTitle)
		
		self.innerPanel = innerPanel
		self.buttonBar = self.createButtons()
		
		self.contentPane.layout = GridBagLayout()
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.PAGE_START  
		c.gridwidth = GridBagConstraints.REMAINDER  
		c.fill = GridBagConstraints.BOTH
		#c.weightx = 1
		#c.weighty = 1
		self.contentPane.add(self.innerPanel,c)
		c.anchor = GridBagConstraints.PAGE_END  
		self.contentPane.add(self.buttonBar,c)
		
		self.contentPane = SnapPanel(self.contentPane)
		
	def closeButton(self, event):
		try:
			Window.setVisible(self, False)
		except Exception, gde:
			Window.hide(self)

	def createButton(self, title, toolTip, actionPerformedMethod):
		button = swing.JButton(title, actionPerformed=actionPerformedMethod)
		button.setToolTipText(toolTip)
		return	button
		
	def createButtons(self):
		# wedge in our controls
		buttonPanel = swing.JPanel();
		buttonPanel.setLayout(BoxLayout(buttonPanel, BoxLayout.X_AXIS))
		buttonPanel.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(''), BorderFactory.createEmptyBorder(10,10,10,10))
		#buttonPanel.add(self.createButton('Close', 'Closes this window', self.closeButton))	
		return buttonPanel

class ButtonBar(JPanel):
	def __init__(self):
		JPanel.__init__(self)
		self.setLayout(BoxLayout(self, BoxLayout.X_AXIS))

	def createButton(self, title, toolTip, actionPerformedMethod):
		button = swing.JButton(title, actionPerformed=actionPerformedMethod)
		button.setToolTipText(toolTip)
		return	button

	def closeButton(self, event):
		try:
			Window.setVisible(self, False)
		except Exception, gde:
			Window.hide(self)
		
	def createButtons(self):
		# wedge in our controls
		#self.add(self.createButton('Close', 'Closes this window', self.closeButton))	
		ignoreMe = 0
				
class Browser(JPanel, HyperlinkListener):
	def __init__(self, prompt,url, width, height):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(prompt), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout =  GridLayout(0,1)
		try:
			print "Loading URL: " + url
			self.urlPane = JEditorPane(url)
		except UnknownHostException:
			print "Error Loading URL: " + url
			self.urlPane = JEditorPane()
			
		self.urlPane.editable = False
		self.urlPane.contentType = "text/html"
		self.urlPane.addHyperlinkListener(self)
		self.control = JScrollPane(self.urlPane,JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS)
		self.control.maximumSize = Dimension(2048,1280)		              
		self.control.preferredSize = Dimension(width,height)
		self.control.minimumSize =Dimension(width,height)
		self.add(self.control)
		offset = 25

		self.maximumSize = Dimension(self.control.maximumSize.width + offset,self.control.maximumSize.height + offset)
		self.preferredSize = Dimension(self.control.preferredSize.width + offset,self.control.preferredSize.height + offset)
		self.minimumSize =Dimension(self.control.minimumSize.width + offset, self.control.minimumSize.height + offset)
		
	def hyperlinkUpdate(self, event):
    		if (event.eventType == HyperlinkEvent.EventType.ACTIVATED):
    			System.out.println(event.description)
	        	self.urlPane.setPage(event.getURL())
	        	#doc = self.urlPane.document
	        	#doc.processHTMLFrameHyperlinkEvent(event)
	        	#self.pack()

class Printer(Printable):
	def __init__(self, printPanel):
		self.printPanel = printPanel

	def Print(self, g, pf, pageIndex):
		g2 = g
		g2.setColor (Color.black)
			
		RepaintManager.currentManager(self.printPanel).setDoubleBufferingEnabled(False)
		
		d = self.printPanel.getSize()
		panelWidth = d.width
		panelHeight = d.height
		pageWidth = pf.getImageableWidth()
		pageHeight = pf.getImageableHeight()
		scale = pageWidth / panelWidth
		totalNumPages = Math.ceil(scale * panelHeight / pageHeight)
		
		if (pageIndex > totalNumPages):
			return Printable.NO_SUCH_PAGE
		
		g2.translate(pf.getImageableX(), pf.getImageableY())
		g2.translate(0, -pageIndex * pageHeight)
		g2.scale(scale, scale)
		self.printPanel.printAll(g2)
		
		return Printable.PAGE_EXISTS

class HTMLPanel(JPanel):
	def __init__(self, prompt, width, height):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(prompt), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout =  GridLayout(0,1)
		self.textPane = JEditorPane()
		self.textPane.contentType = 'text/html'
		self.textPane.editable = False
		self.control = JScrollPane(self.textPane,JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS)
		self.control.maximumSize = Dimension(2048,1280)		              
		self.control.preferredSize = Dimension(width,height)
		self.control.minimumSize =Dimension(width,height)
		self.add(self.control)
		offset = 25
		self.maximumSize = Dimension(self.control.maximumSize.width + offset,self.control.maximumSize.height + offset)
		self.preferredSize = Dimension(self.control.preferredSize.width + offset,self.control.preferredSize.height + offset)
		self.minimumSize =Dimension(self.control.minimumSize.width + offset, self.control.minimumSize.height + offset)
		
	def get_text(self):
		return self.textPane    
		
class Text(JPanel):
	def __init__(self, prompt, width, height):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(prompt), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout =  GridLayout(0,1)
		self.textPane = JEditorPane()
		self.control = JScrollPane(self.textPane,JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS)
		self.control.maximumSize = Dimension(2048,1280)		              
		self.control.preferredSize = Dimension(width,height)
		self.control.minimumSize =Dimension(width,height)
		self.add(self.control)
		offset = 25
		self.maximumSize = Dimension(self.control.maximumSize.width + offset,self.control.maximumSize.height + offset)
		self.preferredSize = Dimension(self.control.preferredSize.width + offset,self.control.preferredSize.height + offset)
		self.minimumSize =Dimension(self.control.minimumSize.width + offset, self.control.minimumSize.height + offset)
		
	def get_text(self):
		return self.textPane
		        			
class PromptField(JPanel):
	def __init__(self, prompt,cols):
		JPanel.__init__(self)
		self.label = JLabel(prompt + ': ')
		self.textField = JTextField('', cols)
		self.layout = GridBagLayout()
		c = GridBagConstraints()
		
		self.add(self.label, c)
		c.gridwidth = GridBagConstraints.RELATIVE 
		c.fill = GridBagConstraints.HORIZONTAL
		self.add(self.textField, c)
    	def getTextField(self):
        	return self.textField
    
		
class	FieldGroup(JPanel):
	def __init__(self, prompt):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(prompt), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout = GridBagLayout()

class NamePanel(JPanel):
	def __init__(self):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder('Contact'), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout = GridBagLayout()
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.FIRST_LINE_START
		c.gridwidth = GridBagConstraints.REMAINDER  
				
		self.add(PromptField('First Name', 15), c)
		self.add(PromptField('Last Name',25), c)

class AddressPanel(JPanel):
	def __init__(self, title):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(title), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout = GridBagLayout()
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.FIRST_LINE_START 
		c.gridwidth = GridBagConstraints.REMAINDER  
		
		self.add(PromptField('Street', 15), c)
		self.add(PromptField('City',25), c)
		
		c.gridwidth = GridBagConstraints.RELATIVE
		self.add(PromptField('State',2), c)
		c.gridwidth = GridBagConstraints.REMAINDER
		self.add(PromptField('ZIP',5), c)
		
class ContactButtonBar(ButtonBar):

	def __init__(self, namePanel):
		ButtonBar.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(''), BorderFactory.createEmptyBorder(10,10,10,10))
		self.namePanel = namePanel
		self.layout = GridLayout()
		self.createButtons()
		
	def createButtons(self):
		# wedge in our controls
		ButtonBar.createButtons(self)
		self.add(self.createButton('Save', '', self.saveButton))	
		self.add(self.createButton('Add', '', self.addButton))	
		self.add(self.createButton('Delete', '', self.deleteButton))	
		
	def saveButton(self, event):
		i = 0

	def addButton(self, event):
		i = 0

	def deleteButton(self, event):
		i = 0

class ContactInformation(JPanel):
	def __init__(self):
		JPanel.__init__(self)
		
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder('Contact Information'), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout = GridBagLayout()
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.FIRST_LINE_START
		c.gridwidth = GridBagConstraints.REMAINDER
		c.fill = GridBagConstraints.BOTH
		
		self.namePanel = NamePanel()
		self.nameButtonBar = ContactButtonBar(self.namePanel)
		self.addressPanel = AddressPanel('Address')
		
		c.gridwidth = GridBagConstraints.RELATIVE
		self.add(self.namePanel,c)
		c.gridwidth = GridBagConstraints.REMAINDER
		self.add(self.addressPanel,c)
		c.gridwidth = GridBagConstraints.RELATIVE
		self.add(AddressPanel('Billing Address'),c)
		c.gridwidth = GridBagConstraints.REMAINDER
		self.add(AddressPanel('Shipping Address'),c)
		self.add(Text('Comments', 100, 100),c)
		self.add(TableExample('Details'),c)
		self.add(Browser('Company URL', 'http://www.google.com', 200, 200),c)
		self.add(self.nameButtonBar,c)		


class URLTabs(JTabbedPane):
	def __init__(self):
		JTabbedPane.__init__(self)
		
	def addURL(self, title, url):
		try:
			print "Loading URL: " + url
			self.add(title, Browser(title, url, 480, 680))
		except Exception:
			print "Error loading url: " + url
			i = 0
	
class MainButtonBar(ButtonBar):

	def __init__(self):
		ButtonBar.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(''), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout = GridLayout()
		self.createButtons()
		
	def createButtons(self):
		# wedge in our controls
		ButtonBar.createButtons(self)
		self.add(self.createButton('Run', '', self.runButton))	
		self.add(self.createButton('New Browser', '', self.runBrowserButton))	

	def runButton(self, event):
		dlg = CFDialog('Sample Python Dialog Test', ContactInformation())
		dlg.size = Dimension(800,800)
		dlg.show()

	def runBrowserButton(self, event):
		dlg = CFDialog('Sample Python Browser Dialog Test', Browser('Google', 'http://www.google.com', 480, 680))
		dlg.size = Dimension(480,680)
		dlg.show()

class SourcePanel(JPanel):
	def __init__(self, filename, width, height):
		JPanel.__init__(self)
		self.layout =  GridLayout(0,1)
		summary = ''

		try:
			f = open(filename, 'r')
			for line in f:
				summary = summary + line
		except Exception: 
			summary = 'Unable to open file: ' + filename

		self.border = BorderFactory.createCompoundBorder(
			BorderFactory.createTitledBorder('Source code for this program'), 
			BorderFactory.createEmptyBorder(10,10,10,10))
		
		self.text = JTextPane()
		self.text.text = summary
		self.text.editable = False
				
		self.control = JScrollPane(self.text,JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS)
		self.control.maximumSize = Dimension(2048,1280)		              
		self.control.preferredSize = Dimension(width,height)
		self.control.minimumSize =Dimension(width,height)

		self.add(self.control)
		offset = 25

		self.maximumSize = Dimension(self.control.maximumSize.width + offset,self.control.maximumSize.height + offset)
		self.preferredSize = Dimension(self.control.preferredSize.width + offset,self.control.preferredSize.height + offset)
		self.minimumSize =Dimension(self.control.minimumSize.width + offset, self.control.minimumSize.height + offset)

class LocalSourcePanel(SourcePanel):
	def __init__(self, width, height):
		SourcePanel.__init__(self, sys.argv[0], width, height)

def countLines(filename):
	f = open(filename, 'r')
	
	lineCount = 0
	for line in f:
		lineCount = lineCount + 1
	
	return lineCount
	
wedgeSrc = """<html>
This program was created with %d lines of jython.  Click on the Source tab to see the source code.<br>
Or, if you want, write your own jython/python program, and run it on the Python Interpreter tab by<br>
wedging it in! To learn more about Jython/Python see the Jython Resources tab!<br><br>
Note:  This project was developed under the funding of a Night's And Weekend's Project,<br>
Otherwise known as a NAW project!<br><br>
Typically, NAW projects are underfunded & overdeveloped, yet push technology to its limits.<br>
Unfortunately though, NAW projects have no business objective or purpose; so they can't be sold.<br>
Later NAW code becomes suitable for open source code, or makes its way into production code<br>
during cut and paste operations.<br><br>
def createWedgePanel():<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wedgePanel = JPanel()<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wedgePanel.border = BorderFactory.createCompoundBorder(<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;BorderFactory.createTitledBorder('Come on! Just Wedge It In!- Chuck\'s Jython Swing Code Samples'), <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;BorderFactory.createEmptyBorder(10,10,10,10))<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wedgePanel.layout = GridBagLayout()<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c = GridBagConstraints()<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c.gridwidth = GridBagConstraints.REMAINDER <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wedgePanel.add(JLabel(wedgeSrc), c)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wedgeURL = URL('https://merriam-webster.com/assets/mw/static/art/dict/wedge.gif')<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wedgePanel.add(JLabel(ImageIcon(wedgeURL)), c)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return	wedgePanel<br>
<br>
</html>
	""" % (countLines(sys.argv[0]))	

def createWedgePanel():
	wedgePanel = JPanel()
	print "here"
	wedgePanel.layout = GridBagLayout()
	c = GridBagConstraints()
	c.anchor = GridBagConstraints.NORTH
	c.gridwidth = GridBagConstraints.REMAINDER
	c.fill = GridBagConstraints.BOTH
	wedgePanel.add(ClockPanel("Current Time"),c)
	wedgePanel.add(JLabel(wedgeSrc), c)
	print "here 3"
	wedgeURL = URL('https://merriam-webster.com/assets/mw/static/art/dict/wedge.gif')
	print "here 3a"
	wedgePanel.add(JLabel(ImageIcon(wedgeURL)), c)

	print "here 4"
	return	TopPanel(wedgePanel, 'Come on! Just Wedge It In!')

def createJythonExamples():
	pythonExamples = URLTabs()
	pythonExamples.add('WedgeItIn.py Source', SnapPanel(LocalSourcePanel(400,400)))
	pythonExamples.add('Python Interpreter', SnapPanel(createPythonPanel()))
	pythonExamples.add('Python Interpreter II', SnapPanel(TopPanel(PythonPanel("""
# Run this by wedging it in, and check the output on the console.
provlist = [[0, 1, 2, 3, 4, 5],[5,4,3,2,1,0],[1,2,3,4,5,6]]

for i in provlist:
	print "i now equal to:", i
	for j in i:
		print "j now equal to:", j
		
print "-----------------"
		
		
		
l = 0
while l < 3:
	k = 0
	while k < 6:
		print "element is " + str(provlist[l][k])
		k = k + 1
		
	l = l + 1      	
	"""),'Wedge It In!')))
	return	pythonExamples
	
def createJythonResources():
	jythonUrls = URLTabs()
	jythonUrls.addURL('Jython.org', 'http://www.jython.org/')
	jythonUrls.addURL('Jython Wikipedia', 'http://en.wikipedia.org/wiki/Jython')
	jythonUrls.addURL('Jython Github', 'https://github.com/jython/jython')

	jythonUrls.addURL('Python', 'http://www.python.org')
	jythonUrls.addURL('Python Wikipedia', 'http://en.wikipedia.org/wiki/Python_(programming_language)')
	
	jythonUrls.addTab('Python Examples', createJythonExamples())
	jythonUrls.addTab('IPV6 Examples', TopPanel(createIPV6Samples(), 'IPV6 Examples'))
	return	jythonUrls	
	
	
class PythonFileFilter(FileFilter):
    def __init__(self):
        FileFilter.__init__(self)
        
    def accept(self, fileObj):
        if (fileObj.isDirectory() == True):
            return True
        
        return fileObj.name.endswith('.py')
    
    def getDescription(self):
        return 'Python script - .py'       

class PythonButtons(ButtonBar):
	def __init__(self, pythonPanel):
		ButtonBar.__init__(self)
		self.pythonPanel = pythonPanel
		self.createButtons()
		
	def createButtons(self):
		# wedge in our controls
		ButtonBar.createButtons(self)
		self.add(self.createButton('Wedge It In!', '<html>This will wedge (i.e run) the Python/Jython program below in your environment.<br>Don\'t forget to check stdout!</html>', self.runButton))	
		self.add(self.createButton('Print', 'Print the source panel', self.printButton))	
		self.add(self.createButton('Load', 'Load a python script.', self.loadButton))	
		self.add(self.createButton('Save', 'Save the current python script to a file.', self.saveButton))	
		
		self.add(self.createButton('Clear', 'Clear the source panel', self.clearButton))	

	def loadButton(self, event):
		pythonCode = self.pythonPanel.getCode().get_text().text

		chooser = JFileChooser()
		chooser.dialogTitle = "Python Script Loader"
		chooser.dialogType = JFileChooser.OPEN_DIALOG
		chooser.approveButtonToolTipText = "Jam's a python script from the filesystem into your python interpreter."
		chooser.setFileFilter(PythonFileFilter())
		returnVal = chooser.showOpenDialog(self)
		if(returnVal == JFileChooser.APPROVE_OPTION):
			self.pythonPanel.getCode().get_text().text = readFile(chooser.selectedFile.absolutePath)

	def saveButton(self, event):
		chooser = JFileChooser()
		chooser.dialogTitle = "Python Script Saver"
		chooser.dialogType = JFileChooser.SAVE_DIALOG
		chooser.approveButtonToolTipText = "Save the code from your python interpreter to the filesystem."
		chooser.setFileFilter(PythonFileFilter())
		if (chooser.showSaveDialog(self) != JFileChooser.APPROVE_OPTION):
		    return
		ps = PrintStream(FileOutputStream(chooser.selectedFile.absolutePath))
		ps.println(self.pythonPanel.getCode().get_text().text)
		ps.flush()
		ps.close()	

	def clearButton(self, event):
		self.pythonPanel.getCode().get_text().text = ""
		
	def runButton(self, event):
		pythonCode = self.pythonPanel.getCode().get_text().text
		
		try:
			exec(pythonCode)
		except SyntaxError, e: 
			programResult = 'Syntax Error'
			
	def printButton(self, e):
		job = PrinterJob.getPrinterJob()
		
		ok = job.printDialog()
		if (ok == True):
			try:
				job.setPrintable(Printer(self.pythonPanel.getCode().get_text()), job.defaultPage())
           			
			  	job.print()
			except Exception, err:
			    	i = 0			

sampleCode = """#This is a sample python program for you to modify and run.

#The output below will be written to the console.
for i in "1234567890":
	print i

#This will create a new dialog box using the internal CFDialog Swing class.  
#This is a swing JDialog and you can add other panels, buttons, etc. to it also.
#Change the URL below and, "wedge it in"
dlg = CFDialog('Sample Python Browser Dialog Test', Browser('Google', 'http://www.google.com', 480, 680))
dlg.size = Dimension(480,680)
dlg.show()
"""

class PythonPanel(JPanel):
	def __init__(self, pythonCode):
		JPanel.__init__(self)
		#self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder('Wedge It In!'), BorderFactory.createEmptyBorder(10,10,10,10))
		
		innerPanel = JPanel()
		innerPanel.layout = GridBagLayout()
		#self.layout = GridBagLayout()
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.FIRST_LINE_START
		c.gridwidth = GridBagConstraints.REMAINDER  
		self.pythonCode = Text('Python Program', 800, 800)
		self.pythonCode.get_text().text = pythonCode
		self.buttons = PythonButtons(self)
		innerPanel.add(self.buttons, c)
		c.fill = GridBagConstraints.BOTH
		innerPanel.add(self.pythonCode, c)
		
		self.setLayout(BoxLayout(self, BoxLayout.X_AXIS))
		self.add(innerPanel)
		
	def getCode(self):
		return self.pythonCode
		
def ResizingPanel(innerPanel):
	panel = JPanel()
	panel.layout = GridLayout(0,1)
	panel.add(innerPanel)
	return panel
		
def createPythonPanel():
	panel =	PythonPanel(sampleCode)
	
	return SnapPanel(TopPanel(panel, 'Wedge It In!'))
	
def createJTable():
	return	TableExample('Disneyworld! - Custom JTable Example')
	
class TableExample(JPanel):
	def __init__(self, prompt):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(prompt), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout =  GridLayout(0,1)
		self.table = self.createTable()
		self.control = JScrollPane(self.table,JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS)
		self.add(self.control)
		
	def createTable(self):
		columns = Vector()
		columns.add("First Name")
		columns.add("Last Name")
		columns.add("SSN")
		columns.add("Street")
		columns.add("City")
		columns.add("State")
		columns.add("Zip")
		
		rows = Vector()
		row = Vector()
		row.add("Mickey")
		row.add("Mouse")
		row.add("999-99-1234")
		row.add("1234 Elm Street")
		row.add("Orlando")
		row.add("Florida")
		row.add("34572")
		rows.add(row)
	
		row = Vector()
		row.add("Minnie")
		row.add("Mouse")
		row.add("999-99-1234")
		row.add("1234 Elm Street")
		row.add("Orlando")
		row.add("Florida")
		row.add("34572")
		rows.add(row)
	
		row = Vector()
		row.add("Donald")
		row.add("Duck")
		row.add("999-99-1234")
		row.add("1231 Maple Avenue")
		row.add("Orlando")
		row.add("Florida")
		row.add("34572")
		rows.add(row)
		
		row = Vector()
		row.add("Daffy")
		row.add("Duck")
		row.add("999-99-1234")
		row.add("1231 Maple Avenue")
		row.add("Orlando")
		row.add("Florida")
		row.add("34572")
		rows.add(row)
		table = JTable(rows, columns)
		return table
	
class DayTimeButtons(ButtonBar):
	def __init__(self, dayTimePanel):
		ButtonBar.__init__(self)
		self.dayTimePanel = dayTimePanel
		self.createButtons()
		
	def createButtons(self):
		# wedge in our controls
		ButtonBar.createButtons(self)
		self.add(self.createButton('Day Time', 'Runs a daytime query on the given host.', self.dayTimeButton))
		self.add(self.createButton('Reset', 'Resets the daytime query result.', self.resetDayTimeButton))

	def dayTimeButton(self, event):
		self.dayTimePanel.dayTimeResult.text = 'Running Daytime Query'
		self.dayTimePanel.dayTimeResult.text = readSocket(self.dayTimePanel.hostname.text, self.dayTimePanel.port.value)

	def resetDayTimeButton(self, event):
		self.dayTimePanel.dayTimeResult.text = '<html><br></html>'
	
class DayTimePanel(JPanel):
	def __init__(self, hostName):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder('Day Time Sample'), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout = GridBagLayout()
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.PAGE_START  
		
		self.label = JLabel('Host: ')
		self.add(self.label, c)
		self.hostname = JTextField(hostName, 32)
		self.add(self.hostname, c)

		self.label1 = JLabel('  Port: ')
		self.add(self.label1, c)
		self.port = JSpinner()
		self.port.value = Integer(13)

		c.gridwidth = GridBagConstraints.REMAINDER  
		self.add(self.port, c)

		self.dayTimeResult = JLabel('<html><br></html>')
		self.add(JLabel('<html><br></html>'),c)
		
		c.gridwidth = GridBagConstraints.REMAINDER  

		self.buttons = DayTimeButtons(self)
		self.add(self.buttons, c)
		
		self.add(JLabel('<html><br></html>'),c)
		self.add(self.dayTimeResult, c)

class LookAndFeelButtonBar(ButtonBar):
	def __init__(self):
		ButtonBar.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(''), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout = GridLayout()
		self.createButtons()
		
	def createButtons(self):
		# wedge in our controls
		ButtonBar.createButtons(self)
		info = UIManager.getInstalledLookAndFeels()	
		for look in info:
			self.add(self.createButton(look.name, 'This will set the applications look and feel to ' + look.name, self.lookAndFeelButton))	
			
	def lookAndFeelButton(self, event):
		lookAndfeelName = event.source.text
		info = UIManager.getInstalledLookAndFeels()
		for look in info:
			if (look.name == event.source.text):
				UIManager.setLookAndFeel(look.className)
				
				
class LookAndFeelPanel(JPanel):
	def __init__(self):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder('Look And Feel'), BorderFactory.createEmptyBorder(10,10,10,10))
		self.add(LookAndFeelButtonBar())
		
def createIPV6Samples():
	tabs = JTabbedPane()
	dayTimePanel = JPanel()
	dayTimePanel.layout = GridBagLayout()
	c = GridBagConstraints()
	c.anchor = GridBagConstraints.FIRST_LINE_START
	c.gridwidth = GridBagConstraints.REMAINDER
	c.fill = GridBagConstraints.HORIZONTAL
	
	dayTimePanel.add(TopPanel(DayTimePanel('2610:20:6f15:15::27'), 'Daytime Client - IPV6 Address'),c)
	dayTimePanel.add(TopPanel(DayTimePanel('time-a-g.nist.gov'), 'Daytime Client - Hostname'),c)
	dayTimePanel.add(TopPanel(DayTimePanel('129.6.15.28'), 'Daytime Client - IPV4 Address'),c)
	tabs.add('Daytime', dayTimePanel)
	#tabs.add('IPV6 Multicast', IPV6MulticastPanel())
	
	
	return tabs
	
def createTabs():
	tabs = JTabbedPane()
	
	tabs.add('Jython Wedge', createWedgePanel())
	tabs.add('Source', SnapPanel(LocalSourcePanel(400,400)))
	# tabs.add('Contact Information - Sample Jython Panel', SnapPanel(ContactInformation()))
	tabs.add('Yahoo - Sample Browser Window', Browser('Yahoo', 'http://www.yahoo.com', 480, 680))
	tabs.add('Jython Resources', createJythonResources())
	tabs.add('Jython Examples', createJythonExamples())
	
	tabs.add('Python Interpreter', createPythonPanel())

	# tabs.add('Look And Feel', LookAndFeelPanel())
	
	return tabs

class ClockPanel(JPanel,Runnable):
	def __init__(self, prompt):
		JPanel.__init__(self)
		self.dateFormat = DateFormat.getTimeInstance (DateFormat.DEFAULT)
		self.add(JLabel(prompt))
		self.timeLabel = JLabel()
		self.add(self.timeLabel)
		self.thread = Thread(self)
		self.thread.start()
		
		
	def run(self):
		while(1 == 1):
			try:
				Thread.sleep(1000)
			except Exception, e:
				ignoreMe = 0

			now = Date ()
	    		date_out = self.dateFormat.format (now)
				
			self.timeLabel.text = date_out

class IPV6MulticastSocket:
    def __init__(self, address, multicastPort):
        self.group = InetAddress.getByName(address)
        self.multicastPort = multicastPort
        self.ipv6Wildcard = InetSocketAddress("::", self.multicastPort)
        self.multicastSocket = MulticastSocket(self.ipv6Wildcard)
        self.multicastSocket.joinGroup(self.group)

    def send(self, msg):
        javaString = String(msg)
        packet = DatagramPacket(javaString.bytes, javaString.length(), self.group, self.multicastPort)
        self.multicastSocket.send(packet)
        
    def receive(self, size):
        sb = StringBuffer(size)
        sb.setLength(size)
        buf = String(sb)
        recv = DatagramPacket(buf.bytes, buf.length())
        self.multicastSocket.receive(recv)
        str = String(recv.data, 0, recv.length)
        return str.toString()
    
    def leaveGroup(self):
        self.multicastSocket.leaveGroup(self.group)
        
	        
class IPV6MulticastPanel(JPanel,Runnable):
    def __init__(self):
		JPanel.__init__(self)
		self.layout = GridBagLayout()
		c = GridBagConstraints()
		c.gridwidth = GridBagConstraints.RELATIVE
        	c.fill = GridBagConstraints.HORIZONTAL
		self.multicastSocket = IPV6MulticastSocket('ff12::ffff', 6500)
		self.userid = PromptField('Name', 50)
		c.gridwidth = GridBagConstraints.REMAINDER  
		self.add(self.userid, c)
		c.gridwidth = GridBagConstraints.REMAINDER  
		self.message = PromptField('Message', 50)
		self.add(self.message, c)
		
		c = GridBagConstraints()
		self.add(self.createButton('Send', '', self.sendButton),c)
		c.gridwidth = GridBagConstraints.REMAINDER  
		self.add(self.createButton('Clear', '', self.clearButton),c)
		self.multicastMessage = HTMLPanel('Chat', 600, 200)
		self.add(self.multicastMessage,c)
		self.thread = Thread(self)
		self.thread.start()
    def createButton(self, title, toolTip, actionPerformedMethod):
		button = JButton(title, actionPerformed=actionPerformedMethod)
		button.setToolTipText(toolTip)
		return	button
    def clearButton(self, event):
		self.multicastMessage.get_text().text = ''
		
    def sendButton(self, event):
		self.multicastSocket.send(self.getMessage())
		
    def getMessage(self):
	    return self.userid.getTextField().text + ' says... ' + self.message.getTextField().text
    def run(self):
		while(1 == 1):
		    	msg = self.multicastSocket.receive(512)
		    	self.multicastMessage.get_text().text = msg + '<br>' + self.multicastMessage.get_text().text
		
				
frame = JFrame("Come on! Just Wedge It In! - Chuck\'s Jython Swing Code Samples")
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)

if (1 == 0):
	frame.contentPane.layout = GridBagLayout()
	c = GridBagConstraints()
	c.gridwidth = GridBagConstraints.REMAINDER 
	frame.contentPane.add(createTabs(),c)
	
frame.contentPane.layout = GridLayout(0,1)
#frame.contentPane.add(ClockPanel())
frame.contentPane.add(createTabs())
#frame.contentPane.add(MainButtonBar(),c)
frame.size = Dimension(800,900)
frame.contentPane = SnapPanel(frame.contentPane)
frame.visible = 1
