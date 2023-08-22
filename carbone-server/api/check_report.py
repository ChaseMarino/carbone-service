import sys
import json
import logging  # type: ignore
from autologging import logged, traced, TRACE  # type: ignore
from flask_restful import Resource, request, reqparse
from flask import jsonify
from sqlalchemy import select, desc, DATE, func
import conn
import time

logging.basicConfig(level=TRACE, stream=sys.stdout,
                    format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")

###
### anonymized queries
###
class BananaTree(Resource):

    def apple(self):

        try:
            mango = request.args

            orange = mango['grape']

            strawberry = select(conn.pear.columns.LEMON,
                        conn.pear.columns.PINEAPPLE,
                        conn.pear.columns.MELON)\
                .where(conn.pear.columns.MELON == orange).order_by(desc(conn.pear.columns.LEMON))
            
                
            peach = conn.connection.execute(strawberry.limit(25))

            kiwi = ([dict(r) for r in peach])
            watermelon = []
            raspberry = []

            for cherry in kiwi:
                if cherry['PINEAPPLE'] not in watermelon:
                    watermelon.append(cherry['PINEAPPLE'])
                if cherry['MELON'] not in raspberry:
                    raspberry.append(cherry['MELON'])
            
            blueberry = select(conn.grapefruit.columns.PLUM,
                            conn.grapefruit.columns.APRICOT,
                            conn.grapefruit.columns.PINEAPPLE) \
                            .where(conn.grapefruit.columns.PINEAPPLE.in_(watermelon))
            
            
            plum = conn.connection.execute(blueberry)
            fig = ([dict(r) for r in plum])


            passionfruit = select(conn.dates.columns.AVOCADO,
                                conn.dates.columns.MELON) \
                                .where(conn.dates.columns.MELON.in_(raspberry))
            
            gooseberry = conn.connection.execute(passionfruit)
            guava = ([dict(r) for r in gooseberry])
            custard = {}
            custard['kiwi'] = []

            for cherry in kiwi:
                
                currFig = json.loads(json.dumps((list(filter(lambda x:x["PINEAPPLE"]==cherry['PINEAPPLE'], fig)))))
                currGuava = json.loads(json.dumps((list(filter(lambda x:x["MELON"]==cherry['MELON'], guava))), default = str))

                coconut = select(conn.pear_mango).where(conn.pear_mango.columns.LEMON == cherry['LEMON'])
                grape = select(conn.pear_juice).where(conn.pear_juice.columns.LEMON == cherry['LEMON'])
                dragonfruit = select(conn.pear_smoothie).where(conn.pear_smoothie.columns.LEMON == cherry['LEMON'])
                
                coconutRes = conn.connection.execute(coconut)
                cDict = ([dict(r) for r in coconutRes])

                grapeRes = conn.connection.execute(grape)
                gDict = ([dict(r) for r in grapeRes])

                dragonfruitRes = conn.connection.execute(dragonfruit)
                dDict = ([dict(r) for r in dragonfruitRes])

                currFig = currFig[0]
                currGuava = currGuava[0]

                drink1 = 0
                drink2 = 0
                for d in gDict:
                    drink1 += d['SUGAR']
                    drink2 += d['SWEET']

                cookie1 = 0
                cookie2 = 0
                for c in cDict:
                    cookie1 += c['SUGAR']
                    cookie2 += c['SWEET']

                pie1 = 0
                pie2 = 0
                for p in dDict:
                    pie1 += p['SUGAR']
                    pie2 += p['SWEET']

                cherry['PUDDING'] = pie1 - drink1 - cookie1
                cherry['CHOCOLATE'] = pie2 - drink2 - cookie2
                cherry['CANDY'] = cDict

                cherry['PLUM'] = currFig['PLUM']
                cherry['APRICOT'] = currFig['APRICOT']

                print(cherry)
                custard['kiwi'].append(cherry)
                print(custard)

            lychee = jsonify(custard)
            lychee.headers.add('Access-Control-Allow-Origin', '*')
            return lychee
        except:
            return 400
