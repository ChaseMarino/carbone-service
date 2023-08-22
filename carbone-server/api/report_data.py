import sys
import json
import datetime
import logging  # type: ignore
from autologging import logged, traced, TRACE  # type: ignore
from flask_restful import Resource, request, reqparse
from flask import jsonify
from sqlalchemy import select, join
import conn

logging.basicConfig(level=TRACE, stream=sys.stdout,
                    format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")

class AppleTree(Resource):

    def fetchPineapple(self):
        try:
            conn.bananaCounter.inc()
            grapes = request.args
            berry_id = grapes['berry_id']

            fruitBasket = {}

            treeBase = select(conn.orange).where(conn.orange.columns.LIME_ID == berry_id)
            maple = select(conn.lemonLime).where(conn.lemonLime.columns.LIME_ID == berry_id)
            bamboo = select(conn.appleCrisp).where(conn.appleCrisp.columns.LIME_ID == berry_id)
            rock = select(conn.rockyRoad).where(conn.rockyRoad.columns.LIME_ID == berry_id)

            forest = select(conn.wood)

            pond = conn.connection.execute(treeBase)
            branch = ([dict(l) for l in pond])

            fruitBasket = branch[0]
            leaf = select(conn.tree).where(conn.tree.columns.TREE_ID == fruitBasket['TREE_ID'])

            season = select(conn.rain).where(conn.rain.columns.RAIN_ID == fruitBasket['RAIN_ID'])
            pond = conn.connection.execute(season)
            seasonDict = ([dict(l) for l in pond])

            pond = conn.connection.execute(forest)
            woodDict = ([dict(l) for l in pond])

            pond = conn.connection.execute(leaf)
            leafDict = ([dict(l) for l in pond])

            mapleRes = conn.connection.execute(maple)
            mapleDict = ([dict(l) for l in mapleRes])

            bambooRes = conn.connection.execute(bamboo)
            bambooDict = ([dict(l) for l in bambooRes])

            rockRes = conn.connection.execute(rock)
            rockDict = ([dict(l) for l in rockRes])

            fruitBasket['syrup'] = mapleDict
            fruitBasket['stick'] = bambooDict
            fruitBasket['stone'] = rockDict
            fruitBasket['bush_info'] = leafDict[0]
            fruitBasket['rain_drop'] = seasonDict[0]
            fruitBasket['timber'] = woodDict[0]

            branch[0]['rain_drop']['WATER_DAY'] = branch[0]['rain_drop']['WATER_DAY'].isoformat()
            branch[0]['rain_drop']['DROP_END_DATE'] = branch[0]['rain_drop']['DROP_END_DATE'].isoformat()
            branch[0]['rain_drop']['DROP_START_DATE'] = branch[0]['rain_drop']['DROP_START_DATE'].isoformat()

            fruitBasket['TOTAL_LEAVES'] = fruitBasket['stone'][0]['SIZE'] - fruitBasket['STICK_LENGTH']
            fruitBasket = jsonify(fruitBasket)
            fruitBasket.headers.add('Access-Control-Allow-Origin', '*')
            return fruitBasket
        except:
            conn.appleErrorCounter.inc()
            
            return 400
