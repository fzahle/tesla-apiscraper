import os
import sys
from pathlib import Path

import srtm



def elevationtoinflux(lat, lon, vin, displayname, ts, ifclient, dryrun, logger):
    if not os.path.isfile('srtm.lck.' + str(os.getpid())):
        Path('srtm.lck.' + str(os.getpid())).touch()
        elevation_data = srtm.get_data()
        elevation = elevation_data.get_elevation(lat, lon)
        os.remove('srtm.lck.' + str(os.getpid()))
        logger.debug("Elevation: " + str(elevation))
        elev_json_body = [
            {
                "measurement": "drive_state",
                "tags": {
                    "vin": vin,
                    "display_name": displayname,
                },
                "time": int(ts * 1000000),
                "fields": {
                    "elevation": elevation
                }
            }
        ]

        if not dryrun and elevation is not None:
            ifclient.write_points(elev_json_body)
    else:
        print("Lockfile detected, skipping")
    sys.exit()
