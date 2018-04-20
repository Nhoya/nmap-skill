from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import getLogger
import nmap

LOGGER = getLogger(__name__)

class NmapSkill(MycroftSkill):
    
    def initialize(self):
        scan_intent = IntentBuilder("ScanIntent"). \
            require("ScanKeyword").require("Host").build()
        self.register_intent(scan_intent, self.handle_scan_intent)
        
        local_scan = IntentBuilder("LocalScan"). \
            require("ScanKeyword").require("LocalNetworkKeyword").build()
        self.register_intent(local_scan, self.handle_local_scan)

        simple_local_scan = IntentBuilder("SimpleLocalScan"). \
            require("SimpleKeyword").require("ScanKeyword").require("LocalNetworkKeyword").build()
        self.register_intent(simple_local_scan, self.handle_simple_local_scan)

    def handle_scan_intent(self, message):
        h = message.data.get('utterance').replace('scan ','').replace(' ', '')
        self.nmap_scan(h, '-sT -A')

    def handle_local_scan(self, message):
        self.nmap_scan("192.168.1.*", '-sT -A')

    def handle_simple_local_scan(self, message):
        self.nmap_scan("192.168.1.*", '-sn -A')

    def nmap_scan(self,h, args):
        self.speak("Scan started, this may take a while")
        nm=nmap.PortScanner()
        nm.scan(h, arguments=args)
        if not nm.all_hosts():
            self.speak("Unable to retrieve info on target")
            return
        for host in nm.all_hosts():
            hostname = nm[host].hostname()
            if hostname != "":
                self.speak(hostname+" found on "+host)
            else:
                self.speak(host+" found")
            for proto in nm[host].all_protocols():
                ports = sorted(nm[host][proto].keys())
                for port in ports:
                    service = nm[host][proto][port]
                    self.speak("port "+str(port)+" is "+service['state']+" exposing "+service['name'])

def create_skill():
    return NmapSkill()
