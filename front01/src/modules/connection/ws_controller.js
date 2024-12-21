import { server_url_ws } from "../configs/configs";
import { timerscounter } from "../support/timers";

class WsConnectionController {
    /*
    this.on_proceed_message = function receive_message({ data })
    */
    constructor() {
        this.reconnect()
        timerscounter.create_new(this.constructor.name+"_update_connection", this.update_connection, 1000*60)
        timerscounter.create_new(this.constructor.name, this.send_ping, 1000*1)
        this.last_input_message = {}
        this.last_input_message_timestamp = null
    }

    on_proceed_message = ({data}) =>{

        this.last_input_message = {}
        try{
            this.last_input_message = JSON.parse(data)
            this.last_input_message_timestamp = new Date()
        }catch(e){
            console.log("WsConnectionController.on_proceed_message", e)
        }
    }

    get_last_message = () =>{
        return this.last_input_message
    }

    set_proceed_message_function = (on_proceed_message) => {
        if (this.on_proceed_message) this.close()
        this.on_proceed_message = on_proceed_message
        if (this.websocket)
            if (this.websocket.readyState)
                this.websocket.addEventListener("message", this.on_proceed_message)
    }

    update_connection = () =>{
        if (this.websocket.readyState !== 1){
            try{
                this.reconnect()
            }
            catch (e){

            }

            
        }
    }

    reconnect = () => {
        try{
            this.websocket.removeEventListener("message", this.on_proceed_message)
        }catch (e){}

        try{
            //this.websocket.close()
        }catch (e){}

        
        this.websocket = new WebSocket(server_url_ws);
        this.websocket.addEventListener("message", this.on_proceed_message)

        
    }


    
    send_ping = () =>{
        this.send_cmd("connection", null, "ping", {})
    }

    send_cmd = (level, target, action, params) => {
        if (this.websocket.readyState !== 1) return
        let res = {
            "level": level,
            "target": target,
            "action": action,
            "params": params
        }
        this.websocket.send(JSON.stringify(res));
    }

    close = () => {
        if (this.websocket) this.websocket.removeEventListener("message", this.on_proceed_message)
    }
}

export const ws_connection = new WsConnectionController()
