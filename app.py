from flask import Flask
from main import main_bp
#from game import game_bp
#from story import story_bp

def create_app():
  app = Flask(__name__)

  #Register blueprints
  app.register_blueprint(main_bp)
  #app.register_blueprint(game_bp, url_prefix='/game')
  #app.register_blueprint(story_bp, url_prefix='/story')

  return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)