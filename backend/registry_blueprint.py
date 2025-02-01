from flask import Blueprint, request, g, jsonify
from flask_cors import CORS

registry_bp = Blueprint('registry', __name__)
CORS(registry_bp)


@registry_bp.route('/chassies', methods=['GET'])
def get_chassis():
    result = registry_bp.car_registry.get_chassies()
    return jsonify({"success": True, "data": result}), 200


@registry_bp.route('/cars', methods=['PUT'])
def add_car():
    data = request.get_json()
    registry_bp.car_registry.add_whole_car(g.userId, data['generalInfo'], data['engineInfo'], data['wheelsInfo'])
    return jsonify({"success": True, "data": "Car added with details"}), 200


@registry_bp.route('/<string:chassis>/modifications', methods=['POST'])
def add_modification(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.add_modification(g.userId, chassis, data["partEnum"], data["details"])
    return jsonify({"success": True, "data": "added"}), 200


@registry_bp.route('/<string:chassis>/events', methods=['POST'])
def add_event(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.add_event(g.userId, chassis, data['eventEnum'], data['details'])
    return jsonify({"success": True, "data": "added"}), 200


@registry_bp.route('/<string:chassis>/extras', methods=['POST'])
def add_extra(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.add_extra(g.userId, chassis, data['details'])
    return jsonify({"success": True, "data": "added"}), 200


@registry_bp.route('/chassis', methods=['POST'])
def add_chassis():
    data = request.get_json()
    result = registry_bp.car_registry.add_chassis(g.userId, data['chassis'])
    return jsonify({"success": True, "data": "added"}), 200


# @registry_bp.route('/<string:chassis>/details', methods=['POST'])
# def add_details(chassis):
#     data = request.get_json()
#     result = registry_bp.car_registry.add_details(g.userId, chassis, data['generalInfo'], data['engineInfo'],
#                                                   data['wheelsInfo'])
#     return jsonify({"success": True, "data": result}), 200

@registry_bp.route('/<string:chassis>/transfer', methods=['POST'])
def add_transfer(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.add_transfer(g.userId, chassis, data['transfer'])
    return jsonify({"success": True, "data": result}), 200

@registry_bp.route('/<string:chassis>/general/km', methods=['PUT'])
def modify_km(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.modify_km(g.userId, chassis, data['km'])
    return jsonify({"success": True, "data": result}), 200


@registry_bp.route('/<string:chassis>/general/gearbox', methods=['PUT'])
def modify_gearbox(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.modify_gearbox(g.userId, chassis, data['gearbox'])
    return jsonify({"success": True, "data": result}), 200


@registry_bp.route('/<string:chassis>/general/color', methods=['PUT'])
def modify_color(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.modify_color(g.userId, chassis, data['color'])
    return jsonify({"success": True, "data": result}), 200



@registry_bp.route('/<string:chassis>/general/no_seats', methods=['PUT'])
def modify_no_seats(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.modify_no_seats(g.userId, chassis, data['no_seats'])
    return jsonify({"success": True, "data": result}), 200


@registry_bp.route('/<string:chassis>/general/no_doors', methods=['PUT'])
def modify_no_doors(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.modify_no_doors(g.userId, chassis, data['no_doors'])
    return jsonify({"success": True, "data": result}), 200


@registry_bp.route('/<string:chassis>/general/transmission', methods=['PUT'])
def modify_transmission(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.modify_transmission(g.userId, chassis, data['transmission'])
    return jsonify({"success": True, "data": result}), 200


@registry_bp.route('/<string:chassis>/engine', methods=['PUT'])
def modify_engine(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.modify_engine(g.userId, chassis, data['serial'], data['liters'],
                                                    data['horsepower'], data['fuel_type'])
    return jsonify({"success": True, "data": result}), 200


@registry_bp.route('/<string:chassis>/wheels', methods=['PUT'])
def modify_wheels(chassis):
    data = request.get_json()
    result = registry_bp.car_registry.modify_wheels(g.userId, chassis, data['no_wheels'], data['diameter'],
                                                    data['width'])
    return jsonify({"success": True, "data": result}), 200
