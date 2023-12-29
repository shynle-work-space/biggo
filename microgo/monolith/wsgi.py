from index import app

if __name__ == "__main__":
    from config import config
    app.run("0.0.0.0", port=5000, debug=config.get('run_mode') == 'development')