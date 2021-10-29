import xml.sax.handler

class ClassHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
      self.inTitle = 0
      self.mapping = {}

def startElement(self, rdf:about, attributes):
    if rdf:about == "book":
      self.buffer = ""
      self.isbn = attributes["isbn"]
      elif name == "title":
      self.inTitle = 1

def characters(self, data):
    if self.inTitle:
      self.buffer += data

def endElement(self, name):
    if name == "title":
      self.inTitle = 0
      self.mapping[self.isbn] = self.buffer