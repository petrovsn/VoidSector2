import React from 'react'
import { WsConnectionWidget } from '../widjgets/WsConnectionWidget';
import { PerformanceWidget } from '../widjgets/PerformanceWidget';
import { GameTextInspectorWidget } from '../widjgets/GameTextInspectorWidget';
export class ServerAdminPage extends React.Component {
    render() {
        return <div>
            <WsConnectionWidget />
            <PerformanceWidget />
            <GameTextInspectorWidget/>
        </div>

    }
}
