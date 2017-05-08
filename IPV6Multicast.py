import java.lang.System as System
import java.net.NetworkInterface as NetworkInterface
import java.net.InetAddress as InetAddress
import java.net.InetSocketAddress as InetSocketAddress
import java.net.Inet6Address as Inet6Address
import java.net.MulticastSocket as MulticastSocket
import java.net.DatagramPacket as DatagramPacket
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.util.Vector as Vector
import java.util.HashMap as HashMap
import javax.swing.UIManager as UIManager
import javax.swing.JComponent as JComponent
import javax.swing.JFileChooser as JFileChooser
import javax.swing.JPanel as JPanel
import javax.swing.JLabel as JLabel
import javax.swing.JList as JList
import javax.swing.JSpinner as JSpinner
import javax.swing.BoxLayout as BoxLayout
import javax.swing.BorderFactory as BorderFactory
import javax.swing.JDialog as JDialog
import javax.swing.JFrame as JFrame
import javax.swing.JComboBox as JComboBox
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
import java.awt.GridBagLayout as GridBagLayout
import java.awt.GridBagConstraints as GridBagConstraints
import java.awt.GridLayout as GridLayout
import java.awt.Dimension as Dimension
import java.lang.Thread as Thread
import java.lang.Runnable as Runnable


System.setProperty('java.net.preferIPv6Addresses', 'true')
defaultAddress = 'ff12::ffff'
defaultPort = 6500

def getInterface(iface):
	inetAddresses = iface.getInetAddresses()
	while (inetAddresses.hasMoreElements()):
		address = inetAddresses.nextElement()
		 
		hostAddress = address.getHostAddress()
		indexOf = hostAddress.find('%')
		if (indexOf != -1):
			 return hostAddress[indexOf + 1: len(hostAddress)]

	return ''

def isV6Interface(iface):
	inetAddresses = iface.getInetAddresses()
	while (inetAddresses.hasMoreElements()):
		address = inetAddresses.nextElement()
		hostAddress = address.getHostAddress()
		indexOf = hostAddress.find("%")
		
		if (indexOf != -1):
			return 1
		
	return 0
	
networkInterfaces = NetworkInterface.getNetworkInterfaces()
interfaces = Vector()
networkInterfaceNames = HashMap()
nics = HashMap()
defaultNic = None
 
while (networkInterfaces.hasMoreElements()):
	iface = networkInterfaces.nextElement()

	if (isV6Interface(iface) == 1):
		#System.out.print("Interface Name: " + iface.getName())
		#System.out.println(" Interface: " + getInterface(iface))
		interfaces.add(iface.getName())
		networkInterfaceNames.put(iface.getName(), getInterface(iface))
		nics.put(iface.getName(), iface)
		defaultNic = iface

def getNic(nicName):
	nic =  nics.get(nicName)

	return nic

class IPV6MulticastSocket:
    def __init__(self, multicastPort, newGroup, iface):
    	self.groupAddress = None
        self.multicastPort = multicastPort
        addr = Inet6Address.getByName('::')
        self.ipv6Wildcard = InetSocketAddress(addr, self.multicastPort)
        self.multicastSocket = MulticastSocket(self.ipv6Wildcard)
        self.joinGroup(newGroup, iface)

    def disconnect(self):
	self.multicastSocket.disconnect()
    	
    def send(self, msg):
        javaString = String(msg)
        #System.out.println('group: ')
        #System.out.println(self.groupAddress)
        
        packet = DatagramPacket(javaString.bytes, javaString.length(), self.groupAddress)
        self.multicastSocket.send(packet)
        
    def receive(self, size):
        sb = StringBuffer(size)
        sb.setLength(size)
        buf = String(sb)
        recv = DatagramPacket(buf.bytes, buf.length(), self.groupAddress)
        self.multicastSocket.receive(recv)
        #System.out.print('received from: ')
        #System.out.println(self.group)
        str = String(recv.data, 0, recv.length)
        return str.toString()
    
    def leaveGroup(self):
    	if (self.groupAddress != None):
        	self.multicastSocket.leaveGroup(self.groupAddress, self.iface)
        	self.groupAddress = None
 
    def joinGroup(self, newGroup, iface): 
    	self.leaveGroup()
    	self.group = InetAddress.getByName(newGroup)
    	self.iface = iface
    	
    	self.groupAddress = InetSocketAddress(self.group, self.multicastPort)
        self.multicastSocket.joinGroup(self.groupAddress, self.iface)
        return self
 
class Text(JPanel):
	def __init__(self, prompt, width, height):
		JPanel.__init__(self)
		self.border = BorderFactory.createCompoundBorder(BorderFactory.createTitledBorder(prompt), BorderFactory.createEmptyBorder(10,10,10,10))
		self.layout =  GridLayout(0,1)
		self.textPane = JEditorPane()
		self.textPane.contentType = 'text/html'
		self.textPane.editable = False
		self.control = JScrollPane(self.textPane)
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
		self.textField = JTextField(' ', cols)
	        self.layout = GridBagLayout()
	        c = GridBagConstraints()
	        self.add(self.label, c)
	        c.gridwidth = GridBagConstraints.RELATIVE
	        c.fill = GridBagConstraints.HORIZONTAL
	        self.add(self.textField, c)
		        
    	def getTextField(self):
        	return self.textField

class ComboBoxField(JPanel):
	def __init__(self, prompt,contents):
		JPanel.__init__(self)
		self.label = JLabel(prompt + ': ')
		self.comboBoxField = JComboBox(contents)
	        self.layout = GridBagLayout()
	        c = GridBagConstraints()
	        self.add(self.label, c)
	        c.gridwidth = GridBagConstraints.RELATIVE
	        c.fill = GridBagConstraints.HORIZONTAL
	        
	        self.add(self.comboBoxField, c)
		        
    	def getComboBoxField(self):
        	return self.comboBoxField
    
class IPV6MulticastPanel(JPanel,Runnable):
    def __init__(self):
		JPanel.__init__(self)
		self.layout = GridBagLayout()
		c = GridBagConstraints()
 		self.mcastAddress = PromptField('Multicast Address', 50)
		self.mcastAddress.getTextField().text = defaultAddress
		
		nicName = self.mcastAddress.getTextField().text
		self.multicastSocket = IPV6MulticastSocket(defaultPort, nicName, getNic(defaultNic))
	
		self.userid = PromptField('Name', 20)
		c.anchor = GridBagConstraints.FIRST_LINE_START 
		c.gridwidth = GridBagConstraints.REMAINDER  
		self.add(self.userid, c)
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.FIRST_LINE_START 
		c.gridwidth = GridBagConstraints.REMAINDER  
		self.message = PromptField('Message', 50)
		self.add(self.message, c)
		
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.FIRST_LINE_START 
		c.gridwidth = GridBagConstraints.REMAINDER
		self.add(self.mcastAddress, c)

		c = GridBagConstraints()
		c.anchor = GridBagConstraints.FIRST_LINE_START 
		c.gridwidth = GridBagConstraints.REMAINDER  
		self.interfaceList = ComboBoxField('Interface', interfaces)
		self.add(self.interfaceList, c)
		
		c = GridBagConstraints()
		c.anchor = GridBagConstraints.FIRST_LINE_START 
		 
		self.add(self.createButton('Send', '', self.sendButton),c)
		c = GridBagConstraints()
		c.gridwidth = GridBagConstraints.REMAINDER  
		self.add(self.createButton('Clear', '', self.clearButton),c)
		self.multicastMessage = Text('Chat', 600, 200)
		
		c = GridBagConstraints()
		c.gridwidth = GridBagConstraints.REMAINDER  
		c.anchor = GridBagConstraints.FIRST_LINE_START 
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
		selectedItem = self.interfaceList.getComboBoxField().getSelectedItem()
		selectedInterface = networkInterfaceNames.get(selectedItem)
		newAddress = self.mcastAddress.getTextField().text + '%' + selectedInterface
		#System.out.println('selectedItem')
		#System.out.println(selectedItem)
		
		nicName = self.mcastAddress.getTextField().text
		self.multicastSocket.joinGroup(newAddress, getNic(selectedItem))
		self.multicastSocket.send(self.getMessage())
		
    def getMessage(self):
	    return self.userid.getTextField().text + ' says... ' + self.message.getTextField().text
	    
    def run(self):
		while(1 == 1):
			try:
			    	msg = self.multicastSocket.receive(512)
			    	self.multicastMessage.get_text().text = msg + '<br>' + self.multicastMessage.get_text().text
			    	
			except Exception, e:	
				System.out.println("Exception: " + e.message)	

frame = JFrame("IPV6 Multicast Chat")
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)

frame.layout = GridLayout(0,1)
frame.contentPane.add(IPV6MulticastPanel())
frame.size = Dimension(800,400)
frame.visible = 1


