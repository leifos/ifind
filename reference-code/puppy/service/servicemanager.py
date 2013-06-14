
class ServiceManager(object):
  """Manages a collection of search services for a PuppyIR Service"""
  def __init__(self, config):
    self.config = config
    self.search_services = {}
    super(ServiceManager, self).__init__()
  
  
  def add_search_service(self, obj):
    """Add a search service"""
    from puppy.service.searchservice import SearchService

    what_we_need = SearchService
    if not isinstance(obj, what_we_need):
        raise TypeError('requires %s (received %s)' % (what_we_need, type(obj)))

    self.search_services.setdefault(obj.name, obj)
  
  
  def remove_search_service(self, service_or_name):
    """Removes an exisiting search service"""

    from puppy.service.searchservice import SearchService

    if not isinstance(service_or_name, basestring):
        if not isinstance(service_or_name, SearchService):
            raise TypeError('requires basestring or SearchService')

        service_or_name = service_or_name.name

    if service_or_name not in self.search_services:
        raise ValueError('%s not in services' % service_or_name)

    self.search_services.pop(service_or_name)
