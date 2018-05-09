

class Message:
    def message_search(channel, **kwargs):

        #check for term conditions
        if "terms" in kwargs:
            print(kwargs["terms"])
        
        #check for date predicates
        if "date" in kwargs:
            print(kwargs["date"])
        
        #check for authors predicate
        if "authors" in kwargs:
            print(kwargs["authors"])
        
        #check for attachment predicate
        if "attachments" in kwargs:
            print(kwargs["attachments"])