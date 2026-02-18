from . import donors, donations, inventory, dashboard

def register_routes(app):
    app.register_blueprint(donors.bp)
    app.register_blueprint(donations.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(dashboard.bp)