import { ws_connection } from "../connection/ws_controller";
import { data_storage } from "../support/shared_storage";
class ShipController{
    take_control = (mark_id) =>{
        data_storage.save_data("ShipController.controlled", mark_id)
    }

    //percentage
    engine_acceleration = (power) =>{
        let mark_id = data_storage.get_data("ShipController.controlled")
        ws_connection.send_cmd("ships.engine_sm", `${mark_id}.`, "set_acceleration", {"value":power})
    }

    //left or right
    engine_rotation = (direction) =>{
        let mark_id = data_storage.get_data("ShipController.controlled")
        ws_connection.send_cmd("ships.engine_sm", `${mark_id}.`, "set_rotation", {"value":direction})
    }

    //seconds
    set_prediction_depth = (depth) =>{
        let mark_id = data_storage.get_data("ShipController.controlled")
        ws_connection.send_cmd("ships.engine_sm", `${mark_id}.`, "set_rotation", {"value":depth})
    }
}


export const ship_controller = new ShipController()
