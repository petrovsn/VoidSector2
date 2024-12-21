
import { http_request } from "../connection/http_controller"
import { timerscounter } from "../support/timers"
import { ws_connection } from "../connection/ws_controller"

class ServerAdmin {
    constructor() {
        this.ws_connections = {}
        timerscounter.create_new(this.constructor.name, this.update, 1000)
    }

    onSuccess_update = (data) => {
        console.log("ServerAdmin", data)
        this.ws_connections = data["connections"]
    }

    onFailure_update = (data) => {
        this.ws_connections = {}
    }

    update = () => {
        http_request("/admin/ws_connections", "GET", {}, {}, this.onSuccess_update, this.onFailure_update)
    }

    get_ws_connection_data = () => {
        return this.ws_connections
    }

    get_performance_data = () => {
        let last_input_message = ws_connection.last_input_message

        if ("admin" in last_input_message) {

            if ("performance" in last_input_message["admin"]) {

                return last_input_message["admin"]["performance"]
            }
        }


        return {}
    }
}

export let server_admin = new ServerAdmin()
