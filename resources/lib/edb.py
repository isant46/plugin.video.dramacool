import os
import sqlite3
import xbmc
import xbmcaddon

_profile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
_connection = None
_database = os.path.join(_profile, 'recently_viewed.db')

if not os.path.exists(_profile):
    os.makedirs(_profile)


def add(path):
    _connection.execute('INSERT INTO recently_viewed (path) VALUES (?)', (path,))


def connect():
    global _connection

    if _connection is None:
        _connection = sqlite3.connect(_database)
        create()


def close():
    global _connection

    if _connection is not None:
        _connection.commit()
        _connection.close()
        _connection = None


def create():
    _connection.execute('CREATE TABLE IF NOT EXISTS recently_viewed ('
                        'path TEXT UNIQUE ON CONFLICT REPLACE, '
                        'last_visited DATETIME DEFAULT CURRENT_TIMESTAMP)')


def fetchall():
    cursor = _connection.execute('SELECT path FROM recently_viewed ORDER BY last_visited DESC')

    for (path,) in cursor.fetchall():
        yield path


def remove(path):
    _connection.execute('DELETE FROM recently_viewed WHERE path LIKE ?', (path,))
