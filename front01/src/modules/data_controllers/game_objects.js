
import { http_request } from "../connection/http_controller"
import { ws_connection } from "../connection/ws_controller"
import { timerscounter } from "../support/timers"
export class GameObjectsInspector{
    constructor(){
        this.hObjects = {}
        this.lObjects = {}
        this.cShips = {}
        timerscounter.create_new("GameObjectsInspector.update_hObjects", this.update_hObjects, 1000)
    }

    get_lObjects = () =>{
        return ws_connection.last_input_message["lObjects"]
    }

    get_hObjects = () =>{
        if ("hObjects" in ws_connection.last_input_message){
            return ws_connection.last_input_message["hObjects"]
        }
        return this.hObjects
    }

    update_hObjects = () =>{
        http_request("/game_engine/map", "GET", {}, {}, this.update_hObjects_on_Success)
    }

    update_hObjects_on_Success = (data) =>{
        console.log("GameObjectsInspector.update_hObjects_on_Success", data, this.hObjects)
        this.hObjects = data["hObjects"]
    }

    get_ships = () =>{
        let lObjects = game_object_inspector.get_lObjects()
        let result = []
        for(let mark_id in lObjects){
            if(lObjects[mark_id]['marker_type']==="ObjectShip"){
                result.push(mark_id)
            }
        }
        return result
    }
}


export const game_object_inspector = new GameObjectsInspector()
