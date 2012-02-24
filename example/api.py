import teg
import teg.controller
import model

# Example API implementations

class Page(teg.controller.Controller):
    
    @teg.controller.jsonify
    def get(self, oid = None):
        #create basic query
        query = model.session.query(model.Page)
        
        #apply sorting/filtering if model supports it
        query = self.apply_filtering(model.Page, query)
        query = self.apply_sorting(model.Page, query)
        
        #return jsonified data with paging
        return self.generic_get(query, oid, 'pages')
        
        
class Comment(teg.controller.Controller):
    @teg.controller.jsonify
    def get(self, oid = None):
        query = model.session.query(model.Comment)
        query = self.apply_filtering(model.Comment, query)
        query = self.apply_sorting(model.Comment, query)
        return self.generic_get(query, oid, 'comments')
        
class Tag(teg.controller.Controller):
    @teg.controller.jsonify
    def get(self, oid = None):
        query = model.session.query(model.Tag)
        query = self.apply_filtering(model.Tag, query)
        query = self.apply_sorting(model.Tag, query)
        return self.generic_get(query, oid, 'tags')
