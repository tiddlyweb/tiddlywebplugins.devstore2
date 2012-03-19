

import os, shutil
from tiddlywebplugins.utils import get_store
from tiddlyweb.config import config

from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag

def setup_module(module):
    if os.path.exists('store'):
        shutil.rmtree('store')

    module.store = get_store(config)

def test_put_get():
    bag = Bag('testbag')
    store.put(bag)

    tiddler1 = Tiddler('instore', 'testbag')
    tiddler1.text = 'hi'
    store.put(tiddler1)

    tiddler2 = store.get(Tiddler('instore', 'testbag'))
    assert tiddler2.bag == 'testbag'
    assert tiddler2.text == 'hi'

def test_src_get():
    tiddler = Tiddler('test1', 'common')
    tiddler = store.get(tiddler)

    assert tiddler.bag == 'common'
    assert tiddler.modifier == 'cdent'
    assert '!Hi' in tiddler.text 

    tiddler = Tiddler('test2.js', 'common')
    tiddler = store.get(tiddler)

    assert tiddler.bag == 'common'
    assert tiddler.type == 'text/javascript'
    assert 'alert' in tiddler.text
