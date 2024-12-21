import React from 'react'
import { WsConnectionWidget } from './WsConnectionWidget';
import { PerformanceWidget } from './PerformanceWidget';
import { game_object_inspector } from '../data_controllers/game_objects';
import { timerscounter } from '../support/timers';
import { ship_controller } from '../data_controllers/ship_controller';
import { data_storage } from '../support/shared_storage';
import '../styles/ShipCard.css'

export class ShipsInspectorWidget extends React.Component {
    componentDidMount(){
        timerscounter.create_new(this.constructor.name, (e)=>{
            this.forceUpdate()
        }, 100)
    }
    componentWillUnmount(){
        timerscounter.delete(this.constructor.name)
    }

    get_ships = () =>{
        let ship_marks = game_object_inspector.get_ships()
        let result = []
        for(let i =0; i<ship_marks.length; i++){
            result.push(<ShipCard mark_id={ship_marks[i]}/>)
        }
        return result
    }

     

    render() {
        return <div>
            {this.get_ships()}
        </div>

    }
}


class ShipCard extends React.Component {
    render() {
        let selected = data_storage.get_data("ShipController.controlled") === this.props.mark_id
        let className = 'ShipCard'
        if (selected)
            className = className+" marked_red"
        return <div className={className}>
            <label>mark_id: {this.props.mark_id}</label>
            <button onClick={(e)=>{ship_controller.take_control(this.props.mark_id)}}>take control</button>
        </div>
    }
}
