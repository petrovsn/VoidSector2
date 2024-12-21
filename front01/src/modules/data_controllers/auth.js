import { ws_connection } from "../connection/ws_controller"
import { http_request } from "../connection/http_controller"
import { data_storage } from "../support/shared_storage"
import { timerscounter } from "../support/timers"

class AuthController {
    constructor() {
        this.login = ""
        this.password = ""
        this.auth_token = ""
        this.tabs = []
        timerscounter.create_new("AuthController.update_available_tabs", this.update_available_tabs, 1000)
    }

    is_authed = () => {
        return this.auth_token !== ""
    }

    auth = (ship, login, password) => {
        http_request("auth/login",
            "GET",
            {
                "login": login,
                "ship": ship,
                "password": password
            },
            {},
            this.auth_ws)
    }

    auth_ws = (http_auth_responce) => {
        let auth_token = http_auth_responce["auth_token"]
        this.auth_token = auth_token
        data_storage.save_data("AuthController.auth_token", auth_token)
        ws_connection.send_cmd("connection", null, "auth", { "auth_token": auth_token })
    }

    update_available_tabs = () => {
        if (this.is_authed())
            http_request("auth/tabs_access",
                "GET",
                {},
                {},
                (tabs) => { this.tabs = tabs })
    }

    get_available_tabs = () => {
        return this.tabs
    }


}

export const auth_controller = new AuthController()
