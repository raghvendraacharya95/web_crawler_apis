from flask_restplus import Api

from .crawler_controller import api as ns1

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    title='API For A Web Crawler',
    version='1.0',
    description='Gale Partners Assignment',
    authorizations=authorizations
    # All API metadatas
)

api.add_namespace(ns1)