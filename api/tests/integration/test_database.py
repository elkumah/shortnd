def test_database_connection(db_session):

    connection = db_session.connection()

    assert connection is not None