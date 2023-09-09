from app import db_prod

class Prompt(db_prod.Model):
   id = db_prod.Column('prompt_id', db_prod.Integer, primary_key = True)
   content = db_prod.Column(db_prod.String)
   title = db_prod.Column(db_prod.String)
   num_songs = db_prod.Column(db_prod.Integer)
   rating = db_prod.Column(db_prod.Integer)
   def __repr__(self):
      return f"Prompt(id='{self.id}', content={self.content}, title={self.title}, num_songs={self.num_songs}, rating={self.rating})"

class Response(db_prod.Model):
   id = db_prod.Column('id', db_prod.Integer, primary_key = True)
   song_uri = db_prod.Column('song_uri', db_prod.String)
   prompt_id = db_prod.Column('prompt_id', db_prod.Integer, db_prod.ForeignKey('prompt.prompt_id'))
   prompt = db_prod.relationship('Prompt', backref='prompt')
   def __repr__(self):
      return f"Response(id='{self.id}', song_uri={self.song_uri}, prompt_id={self.prompt_id})"