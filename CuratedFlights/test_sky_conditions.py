from metar import Metar
from metar.Datatypes import distance


def set_flight_rules(metar_obj):
    """Set flight rules based on METAR object."""

    # https://en.wikipedia.org/wiki/Flight_categories
    # based on visibility and ceiling
    # VFR: Visual Flight Rules
    if metar_obj.sky[0][0] == "CLR" and metar_obj.vis.value("SM") >= 5:
        return "VFR"
    # Also VFR: Visual Flight Rules
    elif metar_obj.vis.value("SM") >= 5 and metar_obj.sky[0][1].value("FT") >= 3000:
        return "VFR"
    # MVFR: Marginal Visual Flight Rules
    elif metar_obj.vis.value("SM") >= 3 and metar_obj.sky[0][1].value("FT") >= 1000:
        return "MVFR"
    # IFR: Instrument Flight Rules
    elif metar_obj.vis.value("SM") >= 1 and metar_obj.sky[0][1].value("FT") >= 500:
        return "IFR"
    # LIFR: Low Instrument Flight Rules
    elif metar_obj.vis.value("SM") < 1 or metar_obj.sky[0][1].value("FT") < 500:
        return "LIFR"
    else:
        return "UNKNOWN"


KAMA = "KAMA 211653Z 05012KT 10SM CLR 27/16 A3022 RMK AO2 SLP180 T02670156 $"
KDFW = "KDFW 211715Z 17004KT 10SM -TSRA FEW015 SCT050CB BKN065 OVC130 24/22 A3004 RMK AO2 LTG DSNT N AND SW TSB15 OCNL LTGIC SW-NW-N TS SW-NW-N MOV SE P0001 T02440217 $"


report = Metar.Metar(KDFW, False)
print(f"Reporting for {report.code}")
print(set_flight_rules(report))

report = Metar.Metar(KAMA, False)
print(f"Reporting for {report.code}")
print(set_flight_rules(report))
