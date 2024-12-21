import { useLoader } from '@react-three/fiber'
import React, { useRef } from 'react'
import { TextureLoader } from 'three/src/loaders/TextureLoader'

const basic_level = 0

export function MeshObject(props) {
    const texture = useLoader(TextureLoader, props.texture)
    const meshRef = useRef()
    let scale_factor = props.scale_factor ? props.scale_factor : 1
    let offset_factor = props.offset_factor ? props.offset_factor : [0, 0]

    let position = [0, 0, 0]
    position[0] = props.position[0] * scale_factor - offset_factor[0] * scale_factor
    position[1] = props.position[1] * scale_factor - offset_factor[1] * scale_factor
    position[2] = props.level ? props.level + basic_level : basic_level

    let rotation = props.rotation ? props.rotation : 0
    rotation = rotation / 180 * 3.1415

    let size = 10
    let size_array = [size, size]
    if (props.size) {
        if (typeof (props.size) == typeof ([])) {
            size_array[0] = props.size[0]
            size_array[1] = props.size[1]
        }
        else {
            size_array[0] = props.size
            size_array[1] = props.size
        }
    }

    if (!props.no_scale_size) {
        for (let i in size_array) {
            size_array[i] = size_array[i] * scale_factor
        }
    }

    let min_size = props.min_size ? props.min_size : 1

    for (let i in size_array) {
        if (size_array[i] < min_size) {
            size_array[i] = min_size
        }
    }

    size_array = [size_array[0], size_array[1], 0.1]
    return (
        <mesh
            //{...props}
            ref={meshRef}
            rotation={[0, 0, rotation]}
            position={position}
        >
            <boxGeometry args={size_array} />
            <meshStandardMaterial map={texture} color={props.color ? props.color : 0xffffff} transparent={true} />
        </mesh>
    )
}
