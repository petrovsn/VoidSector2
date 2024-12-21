import React from 'react'
import { save_data, get_data } from '../support/shared_storage'
import { auth_controller } from '../data_controllers/auth'
import { timerscounter } from '../support/timers'
import { get_locale } from '../locales/locales'
import { server_admin } from '../data_controllers/server_admin'

import '../styles/PerformanceWidget.css'

export class PerformanceWidget extends React.Component {
    componentDidMount() {
        timerscounter.create_new(this.constructor.name, (e) => {
            this.forceUpdate()
        }, 100)
    }

    get_statistic_labels = () =>{
        let data = server_admin.get_performance_data()
        let result = []
        for(let k in data){
            result.push(<label>{k}:{data[k]}</label>)
        }
        return result
    }

    render() {
        return (<div className='PerformanceWidget'>
                <b>PerformanceWidget</b>
                {this.get_statistic_labels()}
        </div>)
    }
}
