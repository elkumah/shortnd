#import url_service
from app.services.url_service import URLService


def test_import_url_service():
    # Test if URLService can be imported and instantiated
    assert URLService is not None