import React from 'react'
import { data_storage } from './modules/support/shared_storage';
import { auth_controller } from './modules/data_controllers/auth';
import { PagesNavigation } from './modules/widjgets/PagesNavigation';

import { ServerAdminPage } from './modules/widgetPages/ServerAdminPage';
import { PilotMasterPage } from './modules/widgetPages/PilotMasterPage';

import './modules/styles/Basic.css'
class App extends React.Component {
    componentDidMount(){
        data_storage.onSubscribe("PagesNavigation.selected", "App", (e) => {this.forceUpdate()})
    }

    
    get_main_page_content = () =>{
        let selected = data_storage.get_data("PagesNavigation.selected")
        switch (selected){
            case "admin":
                return <ServerAdminPage/>
            case "pilot_master":
                    return <PilotMasterPage/>
            default:
                return <div></div>
        }
    }
    render() {
        return <div>
            <div><PagesNavigation/> <button onClick={(e)=>{auth_controller.auth("", "admin", "12345")}}> LOGIN </button> <button onClick={(e)=>{data_storage.print()}}> PRINT SHARED DATA </button></div>
            {this.get_main_page_content()}
        </div>

       
    }
}

export default App;
