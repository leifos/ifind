# TODO: refactor this to extend from the base topic/document handler.
# This requires some major refactoring of the base class, so has been left for now.

class EntitiesQRELsHandler(object):
    """
    Creates a data structure for the diversity QRELs.
    Should probably be handed by an ifind document/topic thing, but for now...
    """
    def __init__(self, entities_qrels_path):
        self.__ds = {}
        self.__load(entities_qrels_path)
    
    def __load(self, entities_qrels_path):
        """
        Loads the data structure from the file.
        """
        f = open(entities_qrels_path)
        
        for line in f:
            line = line.strip().split(' ')
            topic = line[0]
            entity = line[1]
            docid = line[2]
            judgement = line[3]
            
            if topic not in self.__ds:
                self.__ds[topic] = {}
            
            if docid not in self.__ds[topic]:
                self.__ds[topic][docid] = {}
            
            if entity not in self.__ds[topic][docid]:
                self.__ds[topic][docid][entity] = judgement
    
    def get_mentioned_entity_count_for_doc(self, topic, docid):
        """
        Given a topic and document combination, returns the number of entities that are mentioned in that
        document. By mentioned, we mean that the judgement for the document/topic/entity is >= 1.
        """
        if topic not in self.__ds or docid not in self.__ds[topic]:
            return 0
        
        count = 0
        entity_ds = self.__ds[topic][docid]
        
        for entity in entity_ds:
            if entity_ds[entity] > 0:
                count = count + 1
        
        return count
    
    
    def get_mentioned_entities_for_doc(self, topic, docid):
        """
        Returns a list of the entity IDs for the given topic/document combination.
        """
        if topic not in self.__ds or docid not in self.__ds[topic]:
            return []
        
        entities = []
        entity_ds = self.__ds[topic][docid]
        
        for entity in entity_ds:
            if entity_ds[entity] > 0:
                entities.append(entity)
        
        return entities