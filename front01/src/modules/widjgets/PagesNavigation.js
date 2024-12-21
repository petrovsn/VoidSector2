import React from 'react'
import { data_storage } from '../support/shared_storage'
import { auth_controller } from '../data_controllers/auth'
import { timerscounter } from '../support/timers'
import { get_locale } from '../locales/locales'

import '../styles/PagesNavigation.css'

export class PagesNavigation extends React.Component {
    componentDidMount() {
        timerscounter.create_new(this.constructor.name, (e) => {
            this.forceUpdate()
        }, 1000)
    }
    componentWillUnmount() {
        timerscounter.delete(this.constructor.name)
    }

    get_tab_label = (tab_name) => {
        return <label onClick={() => {
            data_storage.save_data("PagesNavigation.selected", tab_name)
            this.forceUpdate()
        }}>{tab_name}</label>
    }

    get_tabs_list = () => {
        let tab_list = auth_controller.get_available_tabs()
        let result = []
        for (let i in tab_list) {
            result.push(this.get_tab_label(tab_list[i]))
        }
        return result
    }

    render() {
        return (
            <div class="PagesNavigation dropdown">
                <button class="dropbtn"> {get_locale("PagesNavigation")}</button>
                <div class="dropdown-content">
                    {this.get_tabs_list()}
                </div>
            </div>
        )
    }
}
