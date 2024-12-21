import React from 'react'
import { game_object_inspector } from '../data_controllers/game_objects'

export class GameTextInspectorWidget extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            "text":""
        }
        this.get_game_objects_data("hObjects")
    }

    get_button_panel = () =>{
        return <div>
            <button onClick={(e)=>{this.get_game_objects_data("hObjects")}}>hObjects</button>
            <button onClick={(e)=>{this.get_game_objects_data("lObjects")}}>lObjects</button>
            <button onClick={(e)=>{this.get_game_objects_data("cShips")}}>cShips</button>
        </div>
    }

    get_game_objects_data = (key) =>{
        let objects_data = {}
        if (key === "hObjects"){
            objects_data = game_object_inspector.get_hObjects()   
        }
        else if (key === "lObjects"){
            objects_data = game_object_inspector.get_lObjects()
        }
        else if (key === "cShips"){
            objects_data = game_object_inspector.cShips
        }
        console.log("GameTextInspector", objects_data, JSON.stringify(objects_data), this.state)
        this.setState({"text":JSON.stringify(objects_data)})
    }

    render(){
        return(<div>
            {this.state.text}
            {this.get_button_panel()}
        </div>)
    }


}
