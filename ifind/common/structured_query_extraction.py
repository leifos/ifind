__author__ = 'rose'
"""
This contains the code for more intelligent query extraction
based on the structure of the html
it will include parsing for specific divs
ignoring div id/classes
weighting based on importance of tags
"""
from xml.etree import ElementTree
from copy import deepcopy
from query_generation import BiTermQueryGeneration

class StructuredExtractor():
    """
    constructor takes a string of html and a
    """
    def __init__(self, html):
        self.html=html
        self.xml_tree = ElementTree.fromstring(self.html)
        self.html_doc = HtmlDocument()
        self.unique_id = 0

    def read_html(self):
        """
        reads the html by a depth first search storing all
        details into HtmlElement objects and adding to HtmlDoc
        :return:
        """
        root = self.xml_tree
        print root.tag
        print root.text
        print root.attrib
        #add root
        #add self to document
        elem = HtmlElement(tag = root.tag, id="-1",content=root.text)
        elem.set_position(x=0 ,y=0)
        self.html_doc.add_element(elem)
        self.process_element(elem=root,depth=0)
        self.print_html()

    def process_element(self, elem, depth):
        breadth = -1
        children = elem.getchildren()
        if children:
            depth += 1
        for child in children:
            breadth += 1
            curr_tag = child.tag
            curr_id = self.get_id(child)
            print "id for tag is ", curr_tag , curr_id
            curr_text = child.text
            curr_elem = HtmlElement(tag=curr_tag, id=curr_id, content=curr_text)
            curr_elem.set_position(x=breadth,y=depth)
            self.html_doc.add_element(curr_elem)
            self.process_element(child, depth)


    def print_html(self):
        self.html_doc.print_document()

    def get_id(self, node):
        if "id" in node.attrib:
            id = node.attrib["id"]
            return id
        else:
            self.unique_id += 1
            return self.unique_id

    def remove_div_content(self, div_ids):
        """
        returns a string with the content the html with the content of
        divs in div_ids removed
        :param div_ids: a list of the ids of the div to be removed
        :return: a string with the divs content removed
        """
        result = ''
        tree_copy = deepcopy(self.xml_tree)
        for div_id in div_ids:
            #need to check the children of the root and then their children
            for element in tree_copy:
                #if the child is a div with the target div id then use the parent to
                #remove the child
                if element.tag == 'div' and element.attrib['id'] == div_id:
                    tree_copy.remove(element)
                for child in element:
                    if child.tag == 'div' and child.attrib['id'] == div_id:
                        element.remove(child)
            #now traverse the copy with the div removed and store the results
        for node in tree_copy:
            if node.text:
                result += node.text
                #print "text of node is ", node.text
            for child in node:
                if child.text:
                    #print "text of node is ", child.text
                    result += child.text

        return result

    def get_node_content(self, node_tag):
        """
        pass the tag of text you want in, the text is returned
        None is returned if that node has no text, it
        doesn't look to children till it gets to text
        :param node_tag:
        :return:
        """
        content =''
        #for node in self.xml_tree.iter():
        #    print node.tag, node.attrib, node.text
        for node in self.xml_tree.iter(node_tag):
            if node.text:
                content = content + node.text
            return content


    def get_div_content(self, div_id):
        """
        returns the content of a div with a particular id
        :param div_id:
        :return:
        """
        #get a list of all div Elements
        all_divs= self.xml_tree.iter("div")
        #create a dom object from the string

        for div in all_divs:
            if div.attrib["id"] == div_id:
                #then we have the right div, go through all it's
                #children and gather their content
                content = ''
                for child in div:
                    if child.text:
                        content += child.text
                return content
        #if you get this far then the id doesn't exist, return none
        return None

    def get_all_related_text(self):
        """
        goes through the html and returns a dictionary of strings
        which contain the content of each element, element name
        is the key content is the value
        could remove ignored divs content before creating the list
        :return:
        """
        #iterate through the elements, when you find text get the
        #tag of the element and store it in a dictionary with the
        #key=tag value=text content

        related_text = {}
        #iterate through the elements in the tree adding to
        #dict when tag with content found which is not empty string and id
        for element in self.xml_tree.iter():
            if element.text != ' ':
                related_text[element.attrib["id"]] = [element.text, element.tag]
        return related_text

    def assign_tag_weightings(self):
        """
        each query will have a weighting based on the position of the query
        :return:
        """
        pass


    def get_query_position(self, query, url):
        """
        takes a query and returns the first
        x,y location of the query in the page
        :param query:
        :return:
        """
        #x location is level in tree
        #y location is number of children along from left in that level of tree
        pass

    def create_biterm_queries(self):
        """
        goes through the related_text dictionary and creates a
        query list using bitermquerygen object for each element
        combines into one query list and returns said list
        :return:
        """
        related_text_dic=self.get_all_related_text()
        all_queries = []
        tag_pos=1
        text_pos=0
        for id, content in related_text_dic.iteritems():
            generator = BiTermQueryGeneration()
            queries = generator.extract_queries_from_text(content[text_pos])
            all_queries.extend(queries)
        #todo remove duplicate queries? add to weight because of increased occurrence?
        return all_queries


class HtmlElement():
    """
    Html element contains tag, id, text content, and position in the document
    """
    def __init__(self, tag, id, content=""):
        self.tag = tag
        if id:
            self.id = id
        else:
            self.id="-1"
        if content:
            self.content = content
        else:
            self.content = ""

    def set_position(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def get_id(self):
        return self.id

    def get_location(self):
        return {self.x_pos, self.y_pos}

    def get_content(self):
        return self.content

    def get_tag(self):
        return self.tag

class HtmlDocument():
    """
    A class which contains a collection of HtmlElement objects
    """
    def __init__(self):
        """
        Use a dictionary for the elements, key is id, value is the
        html object
        :return:
        """
        self.html_doc = {}

    def add_element(self, element):
        if not element.get_id in self.html_doc:
            self.html_doc[element.get_id()] = element

    def get_element_by_id(self, target_id):
        if target_id in self.html_doc:
            return self.html_doc[target_id]
        else:
            return None

    def print_document(self):
        for id, elem in self.html_doc.items():
            print "id:content:tag:pos", elem.get_id(), elem.get_content(), elem.get_tag(), elem.get_location()


    #get elements by tag may be useful?










