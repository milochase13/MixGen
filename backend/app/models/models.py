from app import db

class Prompt(db.Model):
   id = db.Column('prompt_id', db.Integer, primary_key = True)
   content = db.Column(db.String)
   title = db.Column(db.String)
   num_songs = db.Column(db.Integer)
   rating = db.Column(db.Integer)
   def __repr__(self):
      return f"Prompt(id='{self.id}', content={self.content}, title={self.title}, num_songs={self.num_songs}, rating={self.rating})"

class Response(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   song_uri = db.Column('song_uri', db.String)
   prompt_id = db.Column('prompt_id', db.Integer, db.ForeignKey('prompt.prompt_id'))
   prompt = db.relationship('Prompt', backref='prompt')
   def __repr__(self):
      return f"Response(id='{self.id}', song_uri={self.song_uri}, prompt_id={self.prompt_id})"