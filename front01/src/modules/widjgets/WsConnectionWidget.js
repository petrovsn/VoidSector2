import React from 'react'

import { server_admin } from '../data_controllers/server_admin'
import { Table } from './common/table'
import { timerscounter } from '../support/timers'
import { long_machingen_viewer } from './support/viewers'
export class WsConnectionWidget extends React.Component {
    componentDidMount(){
        timerscounter.create_new(this.constructor.name, (e)=>{
            this.forceUpdate()
        }, 1000)
    }

    componentWillUnmount(){
        timerscounter.delete(this.constructor.name)
    }
    render() {
        return <div>
            <Table
                content = {server_admin.get_ws_connection_data()}
                keys = {["ws_token", "origin", "last_ping_ago", "authed", "auth_token"]}
                cell_viewers = {{
                    "ws_token":long_machingen_viewer,
                    "auth_token":long_machingen_viewer
                }}
            />
        </div>

       
    }
}
