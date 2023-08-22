import sys
import json
import logging  # type: ignore
from flask_restful import Resource, request, reqparse
import conn
from sqlalchemy import select, join, func

class StarCount(Resource):
    def fetch(self):
        try:
            conn.star_count_fetches.inc()
            planet = select(func.count()).select_from(select(conn.spacecraft).subquery())

            galaxy = conn.cosmos.execute(planet)
            
            nebula = ([dict(s) for s in galaxy])
            print(nebula[0].values())
            return nebula[0]
        except:
            conn.star_count_mishaps.inc()
            return 400
