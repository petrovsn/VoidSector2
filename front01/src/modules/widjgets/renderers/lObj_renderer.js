import { game_object_inspector } from "../../data_controllers/game_objects";
import { MarkerShip, MarkerDot, MarkerDirection } from "./graphics_primitives";
import { data_storage } from "../../support/shared_storage";

class lObjects_renderer {
    constructor() {
        this.scale_factor = 0
        this.offset_factor = [0, 0]
    }
    get_objects_meshes = () => {
        this.scale_factor = data_storage.get_data("Radar.scale")
        let data = game_object_inspector.get_lObjects()
        let output_meshes = []

        for (let mark_id in data) {
            let tmp = this.generate_meches_for_object(data[mark_id])
            output_meshes = output_meshes.concat(tmp)
        }
        return output_meshes
    }

    generate_meches_for_object = (descr) => {
        let meches_pool = []
        try {
            let position = descr["body"]["pos"]
            let marker_type = descr["marker_type"]
            let main_marker = this.get_main_marker_mech(marker_type, position)
            if (!main_marker) return []
            meches_pool.push(main_marker)
            meches_pool = meches_pool.concat(this.get_prediction_track(descr))
            let direction = this.get_direction_mesh(descr)
            if (direction) meches_pool.push(direction)

        }
        catch (e) {
            console.error("lObjects_renderer.generate_meches_for_object", e)
            meches_pool = []
        }

        return meches_pool
    }

    get_main_marker_mech = (marker_type, position) => {
        switch (marker_type) {
            case "ObjectShip": {
                return <MarkerShip
                    position={position}
                    scale_factor={this.scale_factor}
                    offset_factor={this.offset_factor}
                ></MarkerShip>
            }
            default: {
                break
            }
        }
        return null
    }

    get_prediction_track = (descr) => {
        let result = []
        if (!("predictions" in descr)) return []
        for (let i in descr["predictions"]) {
            let position = descr["predictions"][i]
            result.push(<MarkerDot
                position={position}
                scale_factor={this.scale_factor}
                offset_factor={this.offset_factor}
            />
            )
        }
        return result
    }

    get_direction_mesh = (descr) => {
        if (!("direction" in descr)) return null
        return <MarkerDirection
                position={descr["body"]["pos"]}
                rotation = {descr["direction"]}
                scale_factor={this.scale_factor}
                offset_factor={this.offset_factor}
            />
    }

}


export let lObj_renderer = new lObjects_renderer()
