import teg
import teg.controller
import model
import time

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
        
    @teg.controller.jsonify
    def post(self):
        #create a new page
        data = self.get_request_json()
        page = model.Page()
        
        #validate as needed
        for key in data: 
            if data[key]: 
                setattr(page, key, data[key])
        
        #save it with sqlalchemy
        model.session.add(page)
        model.session.commit()
        #return new object
        self.set_status(201)
        return self.generic_get(model.session.query(model.Page), page.id, 'pages')
      
    @teg.controller.jsonify 
    def put(self, oid):
        data = self.get_request_json()
        page = model.session.query(model.Page).filter_by(id = int(oid)).one()
        page.update(data)
        model.session.commit()
        #return modified object
        return self.generic_get(model.session.query(model.Page), page.id, 'pages')
        
    @teg.controller.jsonify 
    def delete(self, oid):
        page = model.session.query(model.Page).filter_by(id = int(oid)).delete()
        model.session.commit()        
        
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
