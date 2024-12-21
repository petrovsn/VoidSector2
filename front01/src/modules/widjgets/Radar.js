import React from 'react'
import { Canvas } from '@react-three/fiber'
import { hObj_renderer } from './renderers/hObj_renderer'
import { lObj_renderer } from './renderers/lObj_renderer'
import { timerscounter } from '../support/timers'
import { data_storage } from '../support/shared_storage'

export class Radar extends React.Component {
    componentDidMount() {
        timerscounter.create_new(this.constructor.name, (e) => {
            this.forceUpdate()
        }, 30)
    }
    componentWillUnmount() {
        timerscounter.delete(this.constructor.name)
    }

    get_lobjects = () => {

    }
    get_gui = () => {

    }

    get_control_block = () => {
        return (<div>
            <input
                type="range"
                min={0.1}
                max={2}
                step={0.02}
                class="slider"
                id="valueForward"
                value={data_storage.get_data("Radar.scale")}//{this.state.scale_factor}
                onChange={(e) => {
                    data_storage.save_data("Radar.scale", e.target.value) }}
            />
        </div>)
    }

    render() {

        return (<div>
            <Canvas
                //resize = {{ scroll: true, debounce: { scroll: 50, resize: 0 } }}
                orthographic={true}

                style={{
                    'width': "600px",
                    'height': "600px",
                    'border': 'solid',
                    'background': 'black'
                }}
            >
                <ambientLight />
                {hObj_renderer.get_objects_meshes()}
                {lObj_renderer.get_objects_meshes()}
            </Canvas>

            {this.get_control_block()}

        </div>)
    }


}
