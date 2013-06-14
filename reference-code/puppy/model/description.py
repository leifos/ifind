# -*- coding: utf8 -*-

class Description(object):
  """
  OpenSearch Description.
  
  Models an OpenSearch Description document. 
  
  See: http://www.opensearch.org/Specifications/OpenSearch/1.1#OpenSearch_description_document
  
  """
  
  def __init__(self):
    """Constructor for Description."""
    super(Description, self).__init__()
    self.short_name = ''
    self.long_name = ''
    self.description = ''
    self.tags = [] # e.g. <Tags>example web</Tags>
    self.conact = ''
    self.urls = [] # e.g. <Url type="application/rss+xml" template="http://example.com/?q={searchTerms}&amp;pw={startPage?}&amp;format=rss"/>
    self.image = [] # e.g. <Image height="64" width="64" type="image/png">http://example.com/websearch.png</Image>
    self.query = {} # e.g. <Query role="example" searchTerms="cat" />
    self.developer = ''
    self.attribution = ''
    self.syndication_right = ''
    self.adult_content = ''
    self.language = ''
    self.output_encoding = ''
    self.input_encoding = ''
  
  
  def write_xml(self):
    """
    Creates XML for an OpenSearch Description document.
    
    Returns:
    
    * description_xml (str): OpenSearch Description document as XML
    
    **TODO code Description.write_xml()**
    
    """
    pass
  
  
  @staticmethod
  def parse_xml(self, oss_xml):
    """
    Parse OpenSearch Description XML.
    
    Parameters:
    
    * oss_xml (str): OpenSearch Description XML
    
    Returns:
    
    * puppy.model.OpenSearch.Description
    
    TODO code Description.parse_xml()
    
    """
    pass
  
