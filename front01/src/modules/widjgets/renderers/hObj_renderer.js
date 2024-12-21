import { game_object_inspector } from "../../data_controllers/game_objects";
import { data_storage } from "../../support/shared_storage";
import { MarkerAsteroid, MarkerCircle } from "./graphics_primitives";

class hObjects_renderer {
    constructor() {
        this.scale_factor = 0
        this.offset_factor = [0, 0]
    }
    get_objects_meshes = () => {
        this.scale_factor = data_storage.get_data("Radar.scale")
        this.offset_factor = [0, 0]
        let data = game_object_inspector.hObjects
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
            let collider_size = descr["marker_type"]
            let main_marker = this.get_main_marker_mesh(marker_type, descr)
            if (!main_marker) return []
            meches_pool.push(main_marker)

            let gravity_radius = this.get_gravity_radius_mesh(descr)
            if (gravity_radius) meches_pool.push(gravity_radius)

            
        }
        catch (e) {
            console.error("hObjects_renderer.generate_meches_for_object", e)
            meches_pool = []
        }

        return meches_pool
    }

    get_main_marker_mesh = (marker_type, descr) => {
        switch (marker_type) {
            case "ObjectAsteroid": {
                return <MarkerAsteroid
                    position={descr["body"]["pos"]}
                    radius={descr["collider_radius"]}
                    scale_factor={this.scale_factor}
                    offset_factor={this.offset_factor}
                ></MarkerAsteroid>
            }
            default: {
                break
            }
        }
        return null
    }


    get_gravity_radius_mesh = (descr) => {
        if (!("gravity_radius" in descr["body"])) return null
        return (
            <MarkerCircle
                position={descr["body"]["pos"]}
                radius = {descr["body"]["gravity_radius"]}
                scale_factor={this.scale_factor}
                offset_factor={this.offset_factor}
            />
        )

    }

}


export let hObj_renderer = new hObjects_renderer()
