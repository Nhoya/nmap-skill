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


    def handle_scan_intent(self, message):
        self.speak('Scanning Target')
        h = message.data.get('utterance').replace('scan ','')
        nm=nmap.PortScanner()
        nm.scan(h, arguments='-sT')
        if not nm.all_hosts():
            self.speak("Unable to retrieve info on target")
            return
        for host in nm.all_hosts():
            # print(k)
            for proto in nm[host].all_protocols():
                ports = sorted(nm[host][proto].keys())
                for port in ports:
                    service = nm[host][proto][port]
                    self.speak("port "+str(port)+" is "+service['state']+" exposing "+service['name'])

def create_skill():
    return NmapSkill()
