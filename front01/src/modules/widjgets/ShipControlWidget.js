import React from 'react'
import { ship_controller } from '../data_controllers/ship_controller'
import { PressableButton } from './common/buttons';

import '../styles/ShipControlWidget.css'

export class ShipControlWidget extends React.Component {
    render() {
        return (
            <div className='ShipControlWidget'>
                <button disabled={true}>__</button>
                <PressableButton
                    onPress={(e) => { ship_controller.engine_acceleration(1) }}
                    onUnpress={(e) => { ship_controller.engine_acceleration(0) }}
                    label="F" />
                <button disabled={true}>__</button>
                <PressableButton onPress={(e) => { ship_controller.engine_rotation("left") }} label="L" />
                <PressableButton 
                onPress={(e) => { ship_controller.engine_acceleration(-1) }} 
                onUnPress={(e) => { ship_controller.engine_acceleration(0) }}label="B" />
                <PressableButton onPress={(e) => { ship_controller.engine_rotation("right") }} label="R" />
            </div>)
    }
}
