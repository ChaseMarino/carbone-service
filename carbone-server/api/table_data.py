from flask_restful import Resource, request, reqparse
from flask import jsonify
import json
from sqlalchemy import select, desc, DATE, func
import conn
import time

class OceanWave(Resource):
    
    def fetch(self):
        try:

            #conn.seashellGather.inc()

            pearls = request.args

            beachside = pearls['beachside']
            tide = pearls['tide']

            if (tide == ''):
                anchor = select(conn.boat.columns.VESSEL_ID,
                                conn.boat.columns.CREW_ID,
                                conn.boat.columns.SAIL_NO,
                                conn.boat.columns.VOYAGE_ID)\
                    .order_by(desc(conn.boat.columns.VESSEL_ID))
            else:
                anchor = select(conn.boat.columns.VESSEL_ID,
                                conn.boat.columns.CREW_ID,
                                conn.boat.columns.SAIL_NO,
                                conn.boat.columns.VOYAGE_ID)\
                    .filter(conn.boat.columns.CREW_ID == tide)\
                    .order_by(desc(conn.boat.columns.VESSEL_ID))
                
            lagoon = conn.connection.execute(anchor.limit(10).offset(beachside))

            sails = ([dict(r) for r in lagoon])
            captains = []
            voyages = []

            for sail in sails:
                if sail['CREW_ID'] not in captains:
                    captains.append(sail['CREW_ID'])
                if sail['VOYAGE_ID'] not in voyages:
                    voyages.append(sail['VOYAGE_ID'])
            
            capSel = select(conn.crew.columns.CREW_FIRST_NAME,
                            conn.crew.columns.CREW_LAST_NAME,
                            conn.crew.columns.CREW_ID) \
                            .where(conn.crew.columns.CREW_ID.in_(captains))
            
            
            lagoon = conn.connection.execute(capSel)
            cap = ([dict(r) for r in lagoon])

            voyageSel = select(conn.voyage.columns.DATE_SET,
                               conn.voyage.columns.VOYAGE_ID) \
                               .where(conn.voyage.columns.VOYAGE_ID.in_(voyages))
            
            lagoon = conn.connection.execute(voyageSel)
            voy = ([dict(r) for r in lagoon])

            for sail in sails:
                currentCap = json.loads(json.dumps((list(filter(lambda x:x["CREW_ID"]==sail['CREW_ID'], cap)))))
                currentVoy = json.loads(json.dumps((list(filter(lambda x:x["VOYAGE_ID"]==sail['VOYAGE_ID'], voy))), default = str))
                currentCap = currentCap[0]
                currentVoy = currentVoy[0]

                sail['CREW_FIRST_NAME'] = currentCap['CREW_FIRST_NAME']
                sail['CREW_LAST_NAME'] = currentCap['CREW_LAST_NAME']
                sail['DATE_SET'] = currentVoy['DATE_SET']

            if (sails == []):
                lagoon = jsonify(sails)
                lagoon.headers.add('Access-Control-Allow-Origin', '*')
                return lagoon
            
            lagoon = jsonify(sails)
            lagoon.headers.add('Access-Control-Allow-Origin', '*')
            return lagoon
        except:
            #conn.seashellErrors.inc()
            return 400
