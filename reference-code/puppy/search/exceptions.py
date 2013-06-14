class SearchEngineError(Exception):
    """ Use for exceptions in which the search engine wrapper fails - this can be for multiple reasons, 
    for example: the lack of a proxy server in config or a search service being down. Callers should respond
    to this, in a way that fails gracefully. """

    def __init__(self, searchEngineName, error, **extras):
      self.searchEngineName = searchEngineName
      self.error = error
      self.extras = extras

    # Standard one line output with no formatting - for logging on a server etc
    def __str__(self):
      errorMessage = "SearchService '{0}' failed with a '{1}': {2}".format(self.searchEngineName, self.error.__class__.__name__, self.error)

      for extra in self.extras:
        errorMessage += ", {0}: {1}".format(extra, self.extras[extra])

      return errorMessage

    # This method outputs the same error message but formats it to be more readable for during app development
    def formattedStr(self):  
      errorMessage = "\n\n!!! SearchService '{0}' failed with a '{1}': {2}\n".format(self.searchEngineName, self.error.__class__.__name__, self.error)

      if self.extras:
        errorMessage += "\nExtra details for the error message\n---------------------------------------"
        i = 1

        for extra in self.extras:
          errorMessage += "\n{0}) {1}: {2} \n".format(i, extra, self.extras[extra])
          i+=1
        
      return errorMessage

class ApiKeyError(Exception):
    """ Use for exceptions in which the API for a wrapper, which requires one, has not been supplied. Callers should
    respond in such a way that the developer, it is not intended for users of an application, are aware of the issue
    and so can take the necessary steps to rectify the issue."""

    def __init__(self, searchEngineName, apiFieldName):
      self.searchEngineName = searchEngineName
      self.apiFieldName = apiFieldName

    def __str__(self):
      return "SearchService '{0}' failed because the API key was not supplied in config with the fieldname: '{1}'.".format(self.searchEngineName, self.apiFieldName)