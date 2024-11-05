from flask import Blueprint, request, jsonify
from flask_cors import CORS

cars_bp = Blueprint('cars', __name__)
CORS(cars_bp)  # , resources={r"/cars/*": {"origins": "*"}})



# from ml.ModelMS import ModelMS
# from ml.ModelCDS import ModelCDS
# from ml.ModelYK import ModelYK
#
#
# modelYK = ModelYK()
# modelYK.load()
#
# modelCDS = ModelCDS()
# modelCDS.load()
#
# modelMS = ModelMS()
# modelMS.load()


@cars_bp.route('/car', methods=['GET'])
def get_all_car():
    chassis = request.args.get('chassis')
    result = cars_bp.car_registry.get_car_all_info(chassis)
    print(result["carInfo"])
    fabricatie = result["carInfo"]["manufacturingYear"]
    km = result["carInfo"]["noKm"]
    averages = cars_bp.car_registry.average_stats(fabricatie, result["eventHistory"])
    result["analisis"] = {"km_years": 0,
                          "men_sel": [0,0],
                            "crash_dam_ser": [0,0]
                            }


    # result["analisis"] = {"km_years": modelYK.predict(fabricatie, km),
    #                       "men_sel": modelMS.predict(averages["avg_mentenances"], averages["avg_sales"]),
    #                       "crash_dam_ser": modelCDS.predict(averages["avg_crashes"], averages["avg_damages"],
    #                                                         averages["avg_services"])
    #                       }
    return jsonify({"success": True, "data": result}), 200


@cars_bp.route('/chassies', methods=['GET'])  # /cars/chassies?chassis=123
def check_car_existence():
    chassis = request.args.get('chassis')
    cars_bp.car_registry.check_car_existence(chassis)
    return jsonify({"success": True, "data": "Car exists"}), 200
