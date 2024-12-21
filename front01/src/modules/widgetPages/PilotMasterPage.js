import React from 'react'


import {Radar} from '../widjgets/Radar.js'
import { ShipsInspectorWidget } from '../widjgets/ShipsInspectorWidget.js'
import { ShipControlWidget } from '../widjgets/ShipControlWidget.js'

export class PilotMasterPage extends React.Component {
    render() {
        return <div>
            <Radar/>
            <ShipsInspectorWidget/>
            <ShipControlWidget/>
        </div>

    }
}
